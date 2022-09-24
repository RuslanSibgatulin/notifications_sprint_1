from handlers.handler import AutoSubscribeUserHandler, TemplateQueueHandler
from models.models import NewUserEvent, ViewEvent

events_config = {
    "registred": {
        "model": NewUserEvent,
        "handlers": [TemplateQueueHandler, AutoSubscribeUserHandler]

    },
    "views": {
        "model": ViewEvent,
    },
}
