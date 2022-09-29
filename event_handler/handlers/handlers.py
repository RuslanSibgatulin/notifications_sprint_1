import logging
from typing import Any, Dict

from core.settings import rabbit_settings
from db.rabbit_exchange import RabbitExchange
from models.models import NoticeTemplate

from .mixins import PostgresMixin, TemplatesMixin

logger = logging.getLogger(__name__)


class NewUserHandler(TemplatesMixin):
    def __init__(self, event: str) -> None:
        super().__init__()
        self.event = event
        self.rabbit = RabbitExchange(rabbit_settings.uri, exchange="Notice")
        self.version = "v1"

    async def rabbit_publish(
        self,
        rabbit: RabbitExchange,
        context: dict,
        template: NoticeTemplate
    ):
        routing_key = self.get_routing_key(template)
        queue_name = f"{template.notice_method}.send-welcome"
        msg = {
            "context": context,
            "template": template.content}
        await rabbit.publish(routing_key, queue_name, msg)

    def get_routing_key(self, template: NoticeTemplate):
        return "{0}.{1}.{2}".format(
            "user-reporting",
            self.version,
            template.notice_trigger
        )

    async def __call__(self, context: Dict[str, Any]) -> None:
        logger.info("User %s queued notice on event <%s>", context["user_id"], self.event)
        for tmpl in await self.get_templates(self.event):
            await self.rabbit_publish(self.rabbit, context, tmpl)


class AutoSubscribeUserHandler(PostgresMixin):
    def __init__(self, event: str):
        super().__init__()
        self.event = event

    async def __call__(self, context: Dict[str, Any]) -> None:
        logger.info(
            "Auto subscribe user %s on event <%s>",
            context["user_id"],
            self.event
        )
        await self.set_user_subscriptions(context["user_id"])


class UserViewsHandler(PostgresMixin):
    def __init__(self, event: str):
        super().__init__()
        self.event = event

    async def __call__(self, context: Dict[str, Any]) -> None:
        if context["percent"] > 90:
            logger.info(
                "Movie %s user %s progress %s on event <%s>",
                context["movie_id"],
                context["user_id"],
                int(context["percent"]),
                self.event
            )
            await self.set_user_views(context["user_id"], context["movie_id"])
