import logging
from typing import Dict, List

from core.settings import pg_settings, redis_settings
from db.aiopg_notice import PostgresInterface
from db.redis import RedisCache
from models.models import NoticeTemplate

logger = logging.getLogger(__name__)


class PostgresMixin:
    def __init__(self):
        self.storage = PostgresInterface(pg_settings.uri)

    async def get_templates_by_trigger(self, trigger: str) -> List[Dict]:
        query = """
            SELECT
                n.id, n.name notice_name,
                tr.name notice_trigger,
                nm.name notice_method,
                nt.content

            FROM notice n
            INNER JOIN notice_trigger tr ON tr.id = n.trigger_id
            INNER JOIN notice_method nm ON nm.id = n.method_id
            INNER JOIN notice_template nt ON nt.id = n.template_id
            WHERE enabled and tr.name='{0}'
        """.format(trigger)
        return await self.storage.get_data(query)

    async def set_user_subscriptions(self, user_id: str):
        query = """
            INSERT INTO notice_user_subscription
            (user_id, enabled, subscription_id, created, modified)
            SELECT '{0}', true, ns.id, now(), now()
            FROM notice_subscription ns WHERE ns.enabled AND ns.auto
            ON CONFLICT DO NOTHING
        """.format(user_id)
        await self.storage.set_data(query)

    async def set_user_views(self, user_id: str, movie_id: str):
        query = """
            INSERT INTO notice_user_views
            (user_id, movie_id, created)
            VALUES ({0}, {1}, Now())
            ON CONFLICT DO NOTHING
        """.format(user_id, movie_id)
        await self.storage.set_data(query)


class TemplatesMixin(PostgresMixin):
    def __init__(self):
        super().__init__()
        self.redis = RedisCache(redis_settings.uri)

    async def load(self, key: str) -> List[dict]:
        templates = await self.get_templates_by_trigger(key)
        logger.debug("Templates by key <%s> loaded %s", key, templates)
        return templates

    async def get_templates(self, key: str) -> List[NoticeTemplate]:
        cache_key = f"Template:{key}:content"
        templates = await self.redis.get(cache_key)
        if not templates:
            templates = await self.load(key)
            await self.redis.set(cache_key, templates)  # Save to cache

        return [
            NoticeTemplate.parse_obj(i) for i in templates
        ]
