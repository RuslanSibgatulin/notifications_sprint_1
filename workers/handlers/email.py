import asyncio
import logging
from typing import Any, Dict

from core.settings import smtp_settings
from handlers.render import TemplateRender

from .models.models import EmailRabbitMessage
from .sender.smtp_sender import EmailSMTPSender

logger = logging.getLogger(__name__)


class Mailer(EmailSMTPSender, TemplateRender):
    def __init__(self) -> None:
        super().__init__(
            smtp_settings.SMTP_USER,
            smtp_settings.SMTP_PASSWORD,
            smtp_settings.SMTP_HOST,
            smtp_settings.SMTP_PORT
        )
        self.method = "email"

    async def __call__(self, data: Dict[str, Any]) -> bool:
        msg = EmailRabbitMessage.parse_obj(data)
        body = await self.render(msg.context.dict(), msg.template)

        logger.info("Notice over <%s>, %s", self.method, body)
        resp = await self.send(
            msg.context.email,
            "Notification",
            body
        )
        await asyncio.sleep(1)
        if resp:
            logger.info("Sending success")
            return True

        logger.warning("Sending failed")
        return False
