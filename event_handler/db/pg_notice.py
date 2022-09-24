from dataclasses import dataclass
from typing import Dict, Generator, List

import psycopg2
from psycopg2.extensions import STATUS_READY
from psycopg2.extensions import connection as pg_connect
from psycopg2.extras import RealDictCursor

from .backoff import backoff


@dataclass
class PostgresInterface:
    dsn: dict
    conn: pg_connect = None
    limit: int = 1000

    @backoff('Postgres.connect')
    def connect(cls) -> bool:
        if not cls.conn or cls.conn.status != STATUS_READY:
            cls.conn = psycopg2.connect(cls.dsn, async_=True)

        return True

    def get_limited_data(cls, query: str) -> Generator:
        if cls.connect():
            with cls.conn.cursor(cursor_factory=RealDictCursor) as cur:
                offset = 0
                while True:
                    limited_query = '{0} LIMIT {1} OFFSET {2}'.format(
                        query, cls.limit, offset)
                    cur.execute(limited_query)

                    page = cur.fetchall()
                    if page:
                        offset += len(page)
                        yield list(map(dict, page))
                    else:
                        break

    def get_data(cls, query: str) -> List[Dict]:
        data = []
        if cls.connect():
            with cls.conn.cursor(cursor_factory=RealDictCursor) as cur:
                cur.execute(query)
                data = cur.fetchall()

        return list(map(dict, data))

    def set_data(cls, query: str) -> bool:
        res = False
        if cls.connect():
            with cls.conn.cursor(cursor_factory=RealDictCursor) as cur:
                cur.execute(query)
                res = True
        return res
