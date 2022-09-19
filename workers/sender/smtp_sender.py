from email.message import EmailMessage
from smtplib import SMTP_SSL
from typing import Optional

from sender.base import EmailSenderInterface


class EmailSMTPSender(EmailSenderInterface):
    def __init__(
            self,
            user: str,
            password: str,
            smtp_host: str,
            smtp_post: int
    ) -> None:
        self.user = user
        self.password = password
        self.smtp_host = smtp_host
        self.smtp_port = smtp_post
        self.server: Optional[SMTP_SSL] = None

    def connect(self) -> None:
        if self.server is None:
            self.server = SMTP_SSL(self.smtp_host, self.smtp_port)
            self.server.login(self.user, self.password)

    def disconnect(self) -> None:
        if self.server is not None:
            self.server.close()

    def send_email(
            self,
            send_from: str,
            send_to: str,
            subject: str,
            template: str
    ) -> None:
        message = EmailMessage()
        message["From"] = send_from
        message["To"] = send_to
        message["Subject"] = subject
        message.add_alternative(template, subtype='html')
        self.server.sendmail(send_from, send_to, message.as_string())
