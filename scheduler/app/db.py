from contextlib import AbstractContextManager, contextmanager
from typing import Callable

import psycopg2
import psycopg2.extras
from psycopg2.extensions import connection


class Database:
    def __init__(self, host: str, port: int, db_name: str) -> None:
        self.host = host
        self.port = port
        self.db_name = db_name

    @contextmanager
    def conn(self) -> Callable[..., AbstractContextManager[connection]]:
        conn: connection = psycopg2.connect(
            host=self.host, port=self.port, database=self.db_name
        )
        conn.cursor_factory = psycopg2.extras.DictCursor()
        try:
            yield conn
        finally:
            conn.close()
