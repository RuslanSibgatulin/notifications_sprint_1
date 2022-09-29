import json
from datetime import datetime, timedelta, timezone
from typing import Any, Generator

from dependency_injector.wiring import Provide, inject

from containers import Container
from deps.auth import BaseAuthService
from models import Template, ViewEvent
from queue_backend.base import BaseQueueBackend
from services.notifications.base import BaseNotificationTask, NotificationTasksRegistry
from services.notifications.events import EventsProvider
from services.notifications.templates import TemplatesProvider


class NotificationTask(BaseNotificationTask):
    @inject
    def __init__(
        self,
        name: str,
        description: str,
        templates_provider: TemplatesProvider = Provide[Container.templates],
    ) -> None:
        self.name = name
        self.description = description
        self._templates_provider = templates_provider

    def __call__(self) -> None:
        template: Template = self._templates_provider.get_template_by_name(self.name)
        for context in self.get_contexts():
            self.publish(template, context)

    def get_contexts(self) -> Generator[dict[str, Any], None, None]:
        raise NotImplementedError

    def get_routing_key(self) -> str:
        return f"scheduled.{self.name}"

    @inject
    def publish(
        self,
        template: Template,
        context: dict[str, Any],
        queue: BaseQueueBackend = Provide[Container.queue],
    ) -> None:
        message = context | {"template": template.content}
        message_json = json.dumps(message).encode("utf-8")
        routing_key = self.get_routing_key()
        queue.publish(routing_key, message_json)


class RecommendContinueWatching(NotificationTask):
    @inject
    def get_contexts(
        self, auth_service: BaseAuthService = Provide[Container.gateways.auth]
    ) -> Generator[dict[str, Any], None, None]:
        view_events = self.get_views()
        user_ids = [view_event.user_id for view_event in view_events]
        users_info = auth_service.get_user_info(user_ids)

        for view_event, user_info in zip(view_events, users_info):
            yield {
                "user_id": user_info.user_id,
                "movie_id": view_event.movie_id,
            }

    @inject
    def get_views(
        self, events_provider: EventsProvider = Provide[Container.events]
    ) -> Generator[ViewEvent, None, None]:
        now = datetime.utcnow()
        return [
            view_event
            for view_event in events_provider.get_view_events()
            if self._created_before(view_event.created, now, timedelta(hours=24))
        ]

    @staticmethod
    def _created_before(created: int, date: datetime, delta: timedelta) -> bool:
        created_datetime = datetime.fromtimestamp(created, tz=timezone.utc)
        return created_datetime <= date - delta


def add_tasks(registry: NotificationTasksRegistry):
    registry.add_task(
        RecommendContinueWatching(name="recommend_continue_watching", description="")
    )
