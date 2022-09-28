import asyncio
import logging
import logging.config
from typing import Callable

import orjson

from core.logger import LOGGING
from core.settings import rabbit_settings, redis_settings
from db.rabbit_exchange import RabbitExchange
from db.redis import RedisCache
from handlers.email import Mailer

logging.config.dictConfig(LOGGING)
logger = logging.getLogger("Notice-Sender")


class NoticeWorker:
    def __init__(self, queue_name: str, handler: Callable) -> None:
        self.redis = RedisCache(redis_settings.uri)
        self.rabbit = RabbitExchange(rabbit_settings.uri, exchange="Notice")
        self.handler = handler
        self.queue_name = queue_name

    async def start(self):
        async for msg in self.rabbit.consume(self.queue_name):
            logger.debug("Process message %s", msg.message_id)
            resp = await self.handler()(orjson.loads(msg.body))
            if resp:
                await msg.ack()
                logger.info("%s - message processing success", msg.message_id)


if __name__ == "__main__":
    ioloop = asyncio.get_event_loop()
    ioloop.run_until_complete(
        NoticeWorker("email.send", Mailer).start()
    )
    ioloop.close()
