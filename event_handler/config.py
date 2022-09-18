from models.models import NewUserEvent, ViewEvent

events_config = {
    "registred": {
        "model": NewUserEvent,

    },
    "views": {
        "model": ViewEvent
    }
}
