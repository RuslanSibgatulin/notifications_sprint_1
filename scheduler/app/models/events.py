from pydantic import BaseModel


class ViewEvent(BaseModel):
    user_id: str
    movie_id: str
    created: int
