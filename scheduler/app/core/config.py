from pydantic import BaseSettings


class AppSettings(BaseSettings):
    debug: bool = False
    port: int = 50051
    max_workers: int = 10

    class Config:
        env_prefix = "app_"


class GatewaysSettings(BaseSettings):
    rabbit_host: str = "127.0.0.1"
    rabbit_port: int = 5672
    rabbit_queue: str = "scheduled.email.send"

    postgres_host: str = "127.0.0.1"
    postgres_port: int = 5432
    postgres_user: str = "notice"
    postgres_password: str = "123qwe"
    postgres_db_name: str = "notice_database"

    class Config:
        env_prefix = "gateways_"


class SchedulerSettings(BaseSettings):
    pass


class Settings(BaseSettings):
    app: AppSettings = AppSettings()
    gateways: GatewaysSettings = GatewaysSettings()
    scheduler: SchedulerSettings = SchedulerSettings()


settings = Settings()

if settings.app.debug:
    from devtools import debug

    debug(settings)
