import asyncio
import datetime
import logging
from typing import Any, Dict
from uuid import UUID

from core.settings import smtp_settings
from handlers.render import EmailRender
from pydantic import BaseModel

from .sender.smtp_sender import EmailSMTPSender

logger = logging.getLogger(__name__)


class UserInfo(BaseModel):
    user_id: UUID
    email: str
    login: str
    event_time: datetime.datetime


class RabbitMessage(BaseModel):
    context: UserInfo
    template: str


class Mailer:
    def __init__(self) -> None:
        self.sender = EmailSMTPSender(
            smtp_settings.SMTP_USER,
            smtp_settings.SMTP_PASSWORD,
            smtp_settings.SMTP_HOST,
            smtp_settings.SMTP_PORT
        )
        self.render = EmailRender()

    async def __call__(self, data: Dict[str, Any]) -> bool:
        msg = RabbitMessage.parse_obj(data)
        body = await self.render.render(msg.context.dict(), msg.template)

        logger.info("Notice over <email>, %s", body)
        resp = await self.sender.send(
            msg.context.email,
            "Notification",
            body
        )
        await asyncio.sleep(5)
        if resp:
            logger.info("Sending success")
            return True
        # else
        logger.warning("Sending failed")
        return False
