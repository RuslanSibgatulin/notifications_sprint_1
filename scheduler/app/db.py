from contextlib import AbstractContextManager, contextmanager
from typing import Callable

import psycopg2
import psycopg2.extras
from psycopg2.extensions import connection


class Database:
    def __init__(
        self, host: str, port: int, user: str, password: str, db_name: str
    ) -> None:
        self.conn_settings = {
            "host": host,
            "port": port,
            "user": user,
            "password": password,
            "database": db_name,
        }

    @contextmanager
    def conn(self) -> Callable[..., AbstractContextManager[connection]]:
        conn: connection = psycopg2.connect(**self.conn_settings)
        conn.cursor_factory = psycopg2.extras.DictCursor()
        try:
            yield conn
        finally:
            conn.close()
