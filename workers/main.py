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
        queue_iter = self.rabbit.consume(queue_name)
        async for message in queue_iter:
            msg = orjson.loads(message.body)
            logger.info("Received %s", msg)
            await message.ack()


if __name__ == "__main__":
    worker = NoticeWorker()
    asyncio.run(worker.consume("emal.send"))
