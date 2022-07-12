import logging
from typing import Any

import psycopg2
from psycopg2.extras import RealDictCursor


class Postgres:
    """
    Client for connection to PostgreSQL
    """

    def __init__(self, host: str, dbname: str, user: str, password: str) -> None:
        self._conn = psycopg2.connect(
            host=host,
            dbname=dbname,
            user=user,
            password=password,
        )
        self._conn.autocommit = True
        self._cur = self._conn.cursor(cursor_factory=RealDictCursor)

    def close_connection(self) -> None:
        if not self._conn:
            return
        if self._cur:
            self._cur.close()
        self._conn.close()

    def execute(self, query: str, args=None) -> None:
        query = query if isinstance(query, str) else str(query)
        log_rec = f'SQL query "{query}" executed'
        if args:
            log_rec += f" with args: {args}"
        self._cur.execute(query, args)
        logging.debug(log_rec)

    def fetchone(self, query: str, args=None) -> dict[Any, Any] | tuple[Any, ...]:
        self.execute(query, args)

        row = self._cur.fetchone()
        if not row:
            return {}
        return row

    def fetchall(self, query: str, args=None) -> list[Any] | list[tuple[Any, ...]]:
        self.execute(query, args)

        rows = self._cur.fetchall()
        if not rows:
            return []
        return rows


pg_client = Postgres
