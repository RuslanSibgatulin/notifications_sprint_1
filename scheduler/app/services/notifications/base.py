from abc import abstractmethod
from typing import Protocol


class BaseNotificationTask(Protocol):
    name: str
    description: str

    @abstractmethod
    def __call__(self) -> None:
        raise NotImplementedError


class NotificationTasksRegistry(Protocol):
    @abstractmethod
    def add_task(self, task: BaseNotificationTask, *args, **kwargs) -> None:
        raise NotImplementedError

    @abstractmethod
    def get_task(self, name: str, *args, **kwargs) -> BaseNotificationTask | None:
        raise NotImplementedError

    @abstractmethod
    def get_tasks(self, *args, **kwargs) -> list[BaseNotificationTask]:
        raise NotImplementedError
