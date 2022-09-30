import datetime
from uuid import UUID

from pydantic import BaseModel


class EmailUserInfo(BaseModel):
    user_id: UUID
    email: str
    login: str
    event_time: datetime.datetime


class PhoneUserInfo(BaseModel):
    user_id: UUID
    phone: str
    login: str
    event_time: datetime.datetime


class TemplateMixin(BaseModel):
    template: str


class EmailRabbitMessage(TemplateMixin):
    context: EmailUserInfo


class SMSRabbitMessage(TemplateMixin):
    context: PhoneUserInfo
