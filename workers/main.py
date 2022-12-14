import asyncio
import logging.config
from enum import Enum, unique
from typing import Callable, List

import orjson
from core.logger import LOGGING
from core.settings import rabbit_settings, redis_settings
from db.rabbit_exchange import RabbitExchange
from db.redis import RedisCache
from handlers.email import Mailer
from handlers.push import PushSender
from handlers.sms import SmsSender

logging.config.dictConfig(LOGGING)
logger = logging.getLogger("Notice-Sender")


@unique
class MessageStates(Enum):
    NoState = None
    InProgress = 1
    Error = 2
    Processed = 3


class NoticeWorker:
    def __init__(self, queue_name: str, handlers: List[Callable]) -> None:
        self.redis = RedisCache(redis_settings.uri)
        self.rabbit = RabbitExchange(rabbit_settings.uri, exchange="Notice")
        self.handlers = handlers
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
                await self.set_message_state(msg.message_id, MessageStates.InProgress)
                res = await self.exec_handlers(msg)
                if res:
                    await msg.ack()
                    await self.set_message_state(msg.message_id, MessageStates.Processed)
                    logger.info("%s - processing success", msg.message_id)
                else:
                    await self.set_message_state(msg.message_id, MessageStates.Error)
                    logger.warning("Queue message %s - processing failed", msg.message_id)

    async def exec_handlers(self, msg) -> bool:
        logger.debug("Process queue message %s", msg.message_id)
        results = []
        for handler in self.handlers:
            resp = await handler()(orjson.loads(msg.body))
            results.append(resp)

        return any(results)


if __name__ == "__main__":
    ioloop = asyncio.get_event_loop()
    tasks = (
        NoticeWorker("email.send-welcome", [Mailer]).start(),
        NoticeWorker("scheduled.email.send", [Mailer]).start(),
        NoticeWorker("sms.send-confirm", [SmsSender]).start(),
        NoticeWorker("push.send-notice", [PushSender]).start(),
    )
    future = asyncio.gather(*tasks)
    try:
        ioloop.run_until_complete(future)
    finally:
        ioloop.close()
