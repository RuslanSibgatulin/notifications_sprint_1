import asyncio
import logging

import orjson

from core.settings import rabbit_settings, redis_settings
from db.redis import RedisCache
from rabbit.rabbit_exchange import RabbitExchange

logger = logging.getLogger("Sender")
logger.setLevel("DEBUG")


class NoticeWorker:
    def __init__(self) -> None:
        self.redis = RedisCache(redis_settings.uri)
        self.rabbit = RabbitExchange(rabbit_settings.uri, exchange="Notice")

    async def consume(self, queue_name: str):
        try:
            async for msg in self.rabbit.consume(queue_name):
                print(msg.body)
        except KeyboardInterrupt:
            logger.info("Stoped")


if __name__ == "__main__":
    worker = NoticeWorker()
    asyncio.run(worker.consume("email.send"))
