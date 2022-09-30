import logging
from typing import Any, Dict

from handlers.render import TemplateRender

from .models.models import EmailRabbitMessage
from .sender.base import SenderInterface

logger = logging.getLogger(__name__)


class PushSender(SenderInterface, TemplateRender):
    def __init__(self) -> None:
        self.method = "push"

    async def __call__(self, data: Dict[str, Any]) -> bool:
        msg = EmailRabbitMessage.parse_obj(data)
        body = await self.render(msg.context.dict(), msg.template)

        logger.info("Notice over <%s>, %s", self.method, body)
        resp = await self.send(
            msg.context.email,
            "Notification",
            body
        )
        if resp:
            logger.info("Sending success")
            return True

        logger.warning("Sending failed")
        return False
