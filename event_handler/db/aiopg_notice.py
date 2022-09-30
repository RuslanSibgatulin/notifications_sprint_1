import logging
from dataclasses import dataclass
from typing import AsyncGenerator, Dict, List

import aiopg
from psycopg2.errors import CannotConnectNow
from psycopg2.extras import RealDictCursor

from .backoff import backoff

logger = logging.getLogger(__name__)


@dataclass
class PostgresInterface:
    dsn: dict
    conn: aiopg.Connection = None
    limit: int = 1000

    def __del__(cls):
        if cls.conn:
            cls.conn.close()

    @backoff("Postgres.connect", logger)
    async def connect(cls):
        if not cls.conn or cls.conn.closed:
            cls.conn = await aiopg.connect(cls.dsn)
            if cls.conn.closed:
                raise CannotConnectNow(
                    "Cannot connect to postgres"
                )
        return True

    async def get_limited_data(cls, query: str) -> AsyncGenerator:
        if await cls.connect():
            async with cls.connect.cursor(
                cursor_factory=RealDictCursor
            ) as cur:
                offset = 0
                while True:
                    limited_query = "{0} LIMIT {1} OFFSET {2}".format(
                        query, cls.limit, offset)
                    await cur.execute(limited_query)

                    page = cur.fetchall()
                    if page:
                        offset += len(page)
                        yield list(map(dict, page))
                    else:
                        break

    async def get_data(cls, query: str) -> List[Dict]:
        data = []
        if await cls.connect():
            async with cls.conn.cursor(cursor_factory=RealDictCursor) as cur:
                await cur.execute(query)
                data = await cur.fetchall()
        return list(map(dict, data))

    async def set_data(cls, query: str) -> bool:
        res = False
        if await cls.connect():
            async with cls.conn.cursor() as cur:
                await cur.execute(query)
                res = True
        return res
