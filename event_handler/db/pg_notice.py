from typing import Dict, List
import psycopg2
from psycopg2.extensions import connection as pg_connect, STATUS_READY
from psycopg2.extras import RealDictCursor
from dataclasses import dataclass
from .backoff import backoff


@dataclass
class PostgresNotice:
    dsn: dict
    conn: pg_connect = None
    limit: int = 1000

    @backoff('PostgresMovies.connect')
    def connect(cls) -> bool:
        if not cls.conn or cls.conn.status != STATUS_READY:
            cls.conn = psycopg2.connect(cls.dsn)

        return True

    def get_limited_data(cls, query: str) -> List[Dict]:
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
        if cls.connect():
            with cls.conn.cursor(cursor_factory=RealDictCursor) as cur:
                cur.execute(query)
                data = cur.fetchall()

            return list(map(dict, data))

    def get_templates_by_trigger(cls, trigger: str) -> List[Dict]:
        query = """
            SELECT
                n.id, n.name notice_name,
                tr.name notice_trigger,
                nm.name notice_method,
                nt.content

            FROM notice n
            INNER JOIN notice_trigger tr ON tr.id = n.trigger_id
            INNER JOIN notice_method nm ON nm.id = n.method_id
            INNER JOIN notice_template nt ON nt.id = n.template_id
            WHERE enabled and tr.name='{0}'
        """.format(trigger)
        return cls.get_data(query)
