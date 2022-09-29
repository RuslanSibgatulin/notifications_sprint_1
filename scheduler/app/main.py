from concurrent import futures

import grpc
from grpc_interceptor import ExceptionToStatusInterceptor

from api import NotificationsSchedulerService
from containers import Container
from core.config import settings
from proto import scheduler_pb2_grpc
from services.notifications.tasks import add_tasks

container = Container()
container.config.from_pydantic(settings)
container.init_resources()
container.wire(modules=["api"], packages=["services"])

registry = container.registry()
add_tasks(registry)


def serve():
    interceptors = [ExceptionToStatusInterceptor()]
    server = grpc.server(
        futures.ThreadPoolExecutor(max_workers=settings.app.max_workers),
        interceptors=interceptors,
    )
    scheduler_pb2_grpc.add_NotificationsSchedulerServicer_to_server(
        NotificationsSchedulerService(), server
    )

    server.add_insecure_port(f"[::]:{settings.app.port}")
    server.start()
    server.wait_for_termination()


if __name__ == "__main__":
    serve()
