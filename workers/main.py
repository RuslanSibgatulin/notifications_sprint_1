import asyncio
import logging
import logging.config
from enum import Enum, unique
from typing import Callable

import orjson
from core.logger import LOGGING
from core.settings import rabbit_settings, redis_settings
from db.rabbit_exchange import RabbitExchange
from db.redis import RedisCache
from handlers.email import Mailer

logging.config.dictConfig(LOGGING)
logger = logging.getLogger("Notice-Sender")


@unique
class MessageStates(Enum):
    NoState = None
    InProgress = 1
    Error = 2
    Processed = 3


class NoticeWorker:
    def __init__(self, queue_name: str, handler: Callable) -> None:
        self.redis = RedisCache(redis_settings.uri)
        self.rabbit = RabbitExchange(rabbit_settings.uri, exchange="Notice")
        self.handler = handler
        self.queue_name = queue_name

    async def get_message_state(self, message_id: str) -> MessageStates:
        return await self.redis.get(f"{self.queue_name}:{message_id}:state")

    async def set_message_state(self, message_id: str, value: MessageStates) -> None:
        await self.redis.set(
            f"{self.queue_name}:{message_id}:state",
            value,
            10 * 60,  # expires in 10 minutes
        )

    async def start(self) -> None:
        async for msg in self.rabbit.consume(self.queue_name):
            if await self.get_message_state(msg.message_id) != MessageStates.InProgress.value:
                logger.debug("Process message %s", msg.message_id)
                await self.set_message_state(msg.message_id, MessageStates.InProgress)
                resp = await self.handler()(orjson.loads(msg.body))
                if resp:
                    await msg.ack()
                    await self.set_message_state(msg.message_id, MessageStates.Processed)
                    logger.info("%s - processing success", msg.message_id)
                else:
                    await self.set_message_state(msg.message_id, MessageStates.Error)
                    logger.warning("Queue message %s - processing failed", msg.message_id)


if __name__ == "__main__":
    ioloop = asyncio.get_event_loop()
    ioloop.run_until_complete(
        NoticeWorker("email.send", Mailer).start()
    )
    ioloop.close()
