import asyncio
import logging
from typing import Any

import orjson
from aio_pika import Channel, DeliveryMode, Message, connect_robust
from aio_pika.pool import Pool

logger = logging.getLogger(__name__)


class RabbitExchange:
    def __init__(self, url: str, exchange: str) -> None:
        self.url = url
        self.exchange_name = exchange
        self.channel_pool: Pool[Any] = None

    async def get_channel_pool(self):
        loop = asyncio.get_event_loop()
        self.channel_pool = Pool(self.get_channel, max_size=10, loop=loop)

    async def get_connection(self):
        return await connect_robust(self.url)

    async def get_connection_pool(self):
        loop = asyncio.get_event_loop()
        return Pool(self.get_connection, max_size=2, loop=loop)

    async def get_channel(self) -> Channel:
        connection_pool = await self.get_connection_pool()
        async with connection_pool.acquire() as connection:
            return await connection.channel()

    async def publish(self, routing_key: str, queue_name: str, msg: dict):
        if not self.channel_pool:
            await self.get_channel_pool()

        async with self.channel_pool.acquire() as channel:
            exchange = await channel.declare_exchange(
                self.exchange_name,
                durable=True
            )

            ready_queue = await channel.declare_queue(
                queue_name, durable=True
            )
            await ready_queue.bind(exchange, routing_key)

            await exchange.publish(
                Message(
                    body=orjson.dumps(msg),
                    delivery_mode=DeliveryMode.PERSISTENT
                ),
                routing_key
            )

    async def consume(self, queue_name: str):
        if not self.channel_pool:
            await self.get_channel_pool()

        async with self.channel_pool.acquire() as channel:
            while True:
                await channel.set_qos(10)

                queue = await channel.declare_queue(
                    queue_name,
                    durable=True,
                    auto_delete=False
                )
                async with queue.iterator() as queue_iter:
                    async for message in queue_iter:
                        msg = orjson.loads(message.body)
                        logger.info("Received %s", msg)
                        await message.ack()
