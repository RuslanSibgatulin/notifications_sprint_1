import pika
from apscheduler.executors.pool import ThreadPoolExecutor
from apscheduler.jobstores.memory import MemoryJobStore
from dependency_injector import containers, providers

from db import Database
from deps.auth import AuthService
from queue_backend.rabbit import RabbitQueueBackend
from services.notifications.events import EventsProvider
from services.notifications.registry import MemoryTasksRegisty
from services.notifications.templates import TemplatesProvider
from services.scheduler import init_scheduler


class Gateways(containers.DeclarativeContainer):

    config = providers.Configuration()

    auth = providers.Factory(AuthService, host=config.auth_host, port=config.auth_port)

    rabbit_conn_params = providers.Factory(
        pika.ConnectionParameters, host=config.rabbit_host, port=config.rabbit_port
    )
    rabbit = providers.Factory(
        pika.BlockingConnection,
        rabbit_conn_params.provided,
    )

    postgres = providers.Singleton(
        Database,
        host=config.postgres_host,
        port=config.postgres_port,
        user=config.postgres_user,
        password=config.postgres_password,
        db_name=config.postgres_db_name,
    )


class Container(containers.DeclarativeContainer):

    config = providers.Configuration()

    gateways = providers.Container(Gateways, config=config.gateways)

    queue = providers.Factory(
        RabbitQueueBackend,
        name=config.gateways.rabbit_queue_name,
        conn=gateways.rabbit,
    )
    events = providers.Factory(
        EventsProvider, conn_factory=gateways.postgres.provided.conn
    )

    templates = providers.Factory(
        TemplatesProvider, conn_factory=gateways.postgres.provided.conn
    )

    registry = providers.Singleton(MemoryTasksRegisty)

    scheduler = providers.Resource(
        init_scheduler,
        jobstores=providers.Dict(default=providers.Factory(MemoryJobStore)),
        executors=providers.Dict(
            default=providers.Factory(ThreadPoolExecutor, max_workers=10)
        ),
    )
