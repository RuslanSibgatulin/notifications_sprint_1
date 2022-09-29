from contextlib import AbstractContextManager
from typing import Callable

from psycopg2.extensions import connection

from models import ViewEvent


class EventsProvider:
    def __init__(self, conn_factory: Callable[..., AbstractContextManager[connection]]):
        self._conn_factory = conn_factory

    def get_view_events(self) -> list[ViewEvent]:
        query = """
            SELECT *
            FROM notice_user_views
        """

        with self._conn_factory() as conn, conn.cursor() as cur:
            cur.execute(query)
            rows = cur.fetchall()

        return [ViewEvent(**row) for row in rows]
