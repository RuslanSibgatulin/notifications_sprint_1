from contextlib import AbstractContextManager
from typing import Callable

from psycopg2.extensions import connection

from models import Template


class TemplatesProvider:
    def __init__(self, conn_factory: Callable[..., AbstractContextManager[connection]]):
        self._conn_factory = conn_factory

    def get_template_by_name(self, name: str) -> list[Template]:
        query = """
            SELECT
                n.name as notification_name,
                nt.content as content
            FROM notice_subscription n
            INNER JOIN notice_template nt ON nt.id = n.template_id
            WHERE enabled and n.name = %s
        """

        with self._conn_factory() as conn, conn.cursor() as cur:
            cur.execute(query, name)
            rows = cur.fetchall()

        return [Template(**row) for row in rows]
