import asyncio
import logging
import logging.config
from typing import Dict, List, NamedTuple, Optional

import orjson
from aiokafka import AIOKafkaConsumer, TopicPartition

from db.pg_notice import PostgresNotice
from db.rabbit_exchange import RabbitExchange
from db.redis import RedisCache
from models.models import NoticeTemplate
from settings import pg_settings

logging.basicConfig(
    format='[%(asctime)s] [%(name)s] [%(levelname)s] > %(message)s'
)
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)  # TODO: logging config


class EventsHandler:
    def __init__(
        self,
        kafka_url: str,
        rabbit: RabbitExchange,
        redis: RedisCache,
        config: dict
    ) -> None:
        self.server = kafka_url
        self.rabbit = rabbit
        self.redis = redis
        self.config = config
        self.version = "v1"

    async def consume(self, topic: str) -> None:
        REDIS_HASH_KEY = f"consumer:{topic}:offset"
        tp = TopicPartition(topic, 0)
        consumer = AIOKafkaConsumer(
            auto_offset_reset='earliest',
            bootstrap_servers=self.server,
            enable_auto_commit=False,
            retry_backoff_ms=500,
            max_poll_interval_ms=60000,
            metadata_max_age_ms=60000,
            value_deserializer=lambda v: orjson.loads(v.decode("utf-8")),)

        await consumer.start()
        consumer.assign([tp])
        try:
            offset = await self.redis.get(REDIS_HASH_KEY)
            if offset:
                consumer.topics
                consumer.seek(tp, offset=offset + 1)
            # Consume messages
            async for msg in consumer:
                context = self.transform(msg)

                if context:
                    for tmpl in self.get_templates(topic):
                        logger.info("Notice %s, template %s", context, tmpl)
                        await self.rabbit_publish(self.rabbit, context, tmpl)
                await self.redis.set(REDIS_HASH_KEY, msg.offset)
        finally:
            await self.redis.close()
            await consumer.stop()

    def get_templates(self, topic: str) -> List[NoticeTemplate]:
        templates = self.config.get(topic).get("templates", [])
        if not templates:
            templates = [
                NoticeTemplate.parse_obj(i) for i in self.load_templates(topic)
            ]
            self.config[topic]["templates"] = templates  # Save to cache
        return templates

    @staticmethod
    def load_templates(topic: str) -> List[Dict]:
        logger.debug("Loading templates for trigger %s", topic)
        storage = PostgresNotice(pg_settings.uri)
        templ = storage.get_templates_by_trigger(topic)
        logger.debug("Trigger %s templates %s", topic, templ)
        return templ

    def transform(self, event: NamedTuple) -> Optional[Dict]:
        obj = event.value | {"event_time": event.timestamp // 1000}
        model = self.config.get(event.topic, {}).get("model", None)
        if model:
            return model.parse_obj(obj).dict()
        else:
            logger.info("No model for topic %s", event.topic)
            return None

    async def rabbit_publish(
        self,
        rabbit: RabbitExchange,
        context: dict,
        template: NoticeTemplate
    ):
        routing_key = self.get_routing_key(template)
        queue_name = self.get_queue_name(template)
        msg = context | {"template": template.content}
        await rabbit.publish(routing_key, queue_name, msg)

    def get_routing_key(self, template: NoticeTemplate):
        return "{0}.{1}.{2}".format(
            "user-reporting",
            self.version,
            template.notice_trigger
        )

    @staticmethod
    def get_queue_name(template: NoticeTemplate):
        return "{0}.send-{1}".format(
            template.notice_method,
            template.notice_name.lower()  # TODO: need stored queue name
        )

    def run(self):
        for topic in self.config:
            asyncio.run(
                self.consume(topic)
            )
