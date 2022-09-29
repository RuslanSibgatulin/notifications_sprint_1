from pika.connection import Connection

from queue_backend.base import BaseQueueBackend


class RabbitQueueBackend(BaseQueueBackend):
    def __init__(self, name: str, conn: Connection):
        self.name = name
        self._channel = conn.channel()

    def publish(self, routing_key: str, message: bytes) -> None:
        self._channel.queue_declare(queue=self.name)
        self._channel.basic_publish(exhange="", routing_key=routing_key, body=message)
