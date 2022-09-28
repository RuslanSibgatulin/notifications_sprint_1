import logging
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from aiosmtplib import SMTP
from core.backoff import aiobackoff

from .base import EmailSenderInterface

logger = logging.getLogger(__name__)


class EmailSMTPSender(EmailSenderInterface):
    def __init__(
            self,
            user: str,
            password: str,
            smtp_host: str,
            smtp_port: int
    ) -> None:
        self.user = user
        self.password = password
        self.smtp_host = smtp_host
        self.smtp_port = smtp_port
        self.server = SMTP(smtp_host, smtp_port)

    @aiobackoff("SMTP.connect", logger)
    async def connect(self) -> bool:
        if not self.server.is_connected:
            logger.debug("Connecting to SMTP %s:%s", self.smtp_host, self.smtp_port)
            res = await self.server.connect()
            logger.debug("Connection response - %s", res)
            if self.user and self.password:
                res = await self.server.login(
                    username=self.user,
                    password=self.password
                )
                logger.debug("Login response - %s", res)
        return self.server.is_connected

    async def disconnect(self) -> None:
        await self.server.quit()

    async def send(
            self,
            send_to: str,
            subject: str,
            template: str
    ) -> bool:
        message = MIMEMultipart("alternative")
        message["From"] = self.user
        message["To"] = send_to
        message["Subject"] = subject
        plain_text_message = MIMEText(subject, "plain", "utf-8")
        html_message = MIMEText(
            template, "html", "utf-8"
        )
        message.attach(plain_text_message)
        message.attach(html_message)
        res = ""
        if await self.connect():
            logger.info("Ready to send email %s", send_to)
            res = await self.server.sendmail(
                self.user,
                [send_to],
                message.as_string()
            )
            res = res[1]
            logger.info("Sending result - %s", res)
            await self.disconnect()

        return True if res == "OK" else False
