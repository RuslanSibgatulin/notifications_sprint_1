from abc import ABC, abstractmethod


class EmailSenderInterface(ABC):
    @abstractmethod
    async def connect(self) -> None:
        pass

    @abstractmethod
    async def send(
            self,
            send_to: str,
            subject: str,
            template: str
    ) -> bool:
        pass

    @abstractmethod
    async def disconnect(self) -> None:
        pass
