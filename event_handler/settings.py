from pydantic import BaseSettings, Field


class KafkaSettings(BaseSettings):
    KAFKA_TOPIC: str = Field("views", env="MOVIE_PROGRESS_TOPIC")
    KAFKA_HOST: str = "localhost"
    KAFKA_PORT: int = 9092

    @property
    def uri(self) -> str:
        return f"{self.KAFKA_HOST}:{self.KAFKA_PORT}"


class PostgreSettings(BaseSettings):
    POSTGRES_HOST: str = "127.0.0.1"
    POSTGRES_PORT: int = 5432
    POSTGRES_USER: str = "notice"
    POSTGRES_PASSWORD: str = "123qwe"
    POSTGRES_DB: str = "notice_database"

    @property
    def uri(self) -> str:
        return "postgres://{0}:{1}@{2}:{3}/{4}".format(
            self.POSTGRES_USER,
            self.POSTGRES_PASSWORD,
            self.POSTGRES_HOST,
            self.POSTGRES_PORT,
            self.POSTGRES_DB
        )


class RabbitSettings(BaseSettings):
    RABBIT_HOST: str = "127.0.0.1"
    RABBIT_PORT: int = 5672
    RABBIT_USER: str = "guest"
    RABBIT_PASSWORD: str = "guest"
    RABBIT_CONN_ATTEMPTS: int = 3

    @property
    def uri(self) -> str:
        return """amqp://{0}:{1}@{2}:{3}/%2F?connection_attempts={4}&heartbeat=3600
        """.format(
            self.RABBIT_USER,
            self.RABBIT_PASSWORD,
            self.RABBIT_HOST,
            self.RABBIT_PORT,
            self.RABBIT_CONN_ATTEMPTS
        )


class RedisSettings(BaseSettings):
    REDIS_HOST: str = "127.0.0.1"
    REDIS_PORT: int = 6379
    REDIS_DB_INDEX: int = 0

    @property
    def uri(self) -> str:
        return "redis://{0}:{1}/{2}".format(
            self.REDIS_HOST,
            self.REDIS_PORT,
            self.REDIS_DB_INDEX
        )


redis_settings = RedisSettings()
rabbit_settings = RabbitSettings()
pg_settings = PostgreSettings()
kafka_settings = KafkaSettings()
