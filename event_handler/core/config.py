from handlers.handlers import (AutoSubscribeUserHandler, NewUserHandler,
                               UserViewsHandler)
from models.models import NewUserEvent, ViewEvent

events_config = {
    "registred": {
        "model": NewUserEvent,
        "handlers": [NewUserHandler, AutoSubscribeUserHandler]

    },
    "views": {
        "model": ViewEvent,
        "handlers": [UserViewsHandler]
    },
}
