from pydantic import BaseModel


class UserInfo(BaseModel):
    user_id: str
    username: str
    email: str
