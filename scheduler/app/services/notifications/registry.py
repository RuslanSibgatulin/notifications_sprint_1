from services.notifications.base import BaseNotificationTask, NotificationTasksRegistry


class MemoryTasksRegisty(NotificationTasksRegistry):
    def __init__(self) -> None:
        self._registry: dict[str, BaseNotificationTask] = {}

    def add_task(self, task: BaseNotificationTask) -> None:
        self._registry[task.name] = task

    def get_task(self, name: str) -> BaseNotificationTask | None:
        return self._registry.get(name)

    def get_tasks(self) -> list[BaseNotificationTask]:
        return list(self._registry.values())
