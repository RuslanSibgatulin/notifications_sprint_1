from pydantic import BaseSettings


class AppSettings(BaseSettings):
    debug: bool = False
    host: str = "0.0.0.0"
    port: int = 50061
    max_workers: int = 10

    class Config:
        env_prefix = "app_"


settings = AppSettings()

if settings.debug:
    from devtools import debug

    debug(settings)
