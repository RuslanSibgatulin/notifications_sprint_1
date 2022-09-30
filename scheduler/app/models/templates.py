from pydantic import BaseModel


class Template(BaseModel):
    notification_name: str
    content: str
