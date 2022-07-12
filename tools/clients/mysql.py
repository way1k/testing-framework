import logging
import time
from typing import Any, Callable

import pymysql
from pymysql.constants import CLIENT


class MySQL:
    """
    Client for connection to MySQL
    """

    def __init__(
        self,
        host: str,
        database: str,
        user: str,
        password: str,
        shard_name: str | None = None,
        shard_quantity: str | None = None,
        shard_quantity_from: str | None = None,
        shard_quantity_to: str | None = None,
    ):

        self.shard_name = shard_name
        self.shard_quantity = shard_quantity
        self.shard_quantity_from = shard_quantity_from
        self.shard_quantity_to = shard_quantity_to
        self.shard_number = None
        self._conn = pymysql.connect(
            host=host,
            database=database,
            user=user,
            password=password,
            autocommit=True,
            cursorclass=pymysql.cursors.DictCursor,
            connect_timeout=500,
            read_timeout=10,
            write_timeout=10,
            client_flag=CLIENT.MULTI_STATEMENTS,
        )
        self._cur = self._conn.cursor()

    def close_connection(self):
        if not self._conn:
            return
        if self._cur:
            self._cur.close()
        self._conn.close()

    def execute(self, query: str, args=None) -> None:
        self._conn.ping()
        query = query if isinstance(query, str) else str(query)
        log_rec = f'SQL query "{query}" executed'
        if args:
            log_rec += f" with args: {args}"
        self._cur.execute(query, args)
        logging.debug(log_rec)

    def fetchone_result(
        self, query: str, wait_retries: int | None = None, retries_delay: int = 5
    ) -> dict[Any, Any] | tuple[Any, ...]:
        if wait_retries:
            actual_retries = 0
            while 1:
                self.execute(query)
                row = self._cur.fetchone()
                if actual_retries > 0:
                    logging.debug(f"Repeat request №{actual_retries}")
                if row == {} or row == () or row is None:
                    actual_retries += 1
                    if actual_retries == wait_retries:
                        raise AssertionError(
                            "The query returns an empty answer, check your query or database connection"
                        )
                    time.sleep(retries_delay)
                else:
                    return row
        else:
            self.execute(query)
            row = self._cur.fetchone()
            if not row:
                return {}
            return row

    def fetchall_results(
        self, query: str, wait_retries: int | None = None, retries_delay: int = 5
    ) -> list[Any] | tuple[Any, ...]:
        if wait_retries:
            actual_retries = 0
            while 1:
                self.execute(query)
                rows = self._cur.fetchall()
                if actual_retries > 0:
                    logging.debug(f"Repeat request №{actual_retries}")
                if (rows == []) or (rows == [{}]) or (rows == ()) or len(rows) == 0:
                    actual_retries += 1
                    if actual_retries == wait_retries:
                        raise AssertionError(
                            "The query returns an empty answer, check your query or database connection"
                        )
                    time.sleep(retries_delay)
                else:
                    return rows
        else:
            self.execute(query)
            rows = self._cur.fetchall()
            if not rows:
                return []
            return rows

    def query_to_shards(
        self, query_func: Callable[[Any], Any], query_func_args: str | int | None = None
    ) -> dict[Any, Any] | list[Any] | tuple[Any, ...]:
        result = None
        shards = None
        if self.shard_quantity:
            shards = range(1, int(self.shard_quantity) + 1)
        elif self.shard_quantity_from and self.shard_quantity_to:
            shards = range(int(self.shard_quantity_from), int(self.shard_quantity_to) + 1)
        if self.shard_number:
            self._use_database(self.shard_name, self.shard_number)
            return query_func(*query_func_args)
        for shard in shards:
            logging.debug(f"Using shard №{shard}")
            self._use_database(self.shard_name, shard)
            result = query_func(*query_func_args)
            if len(result) == 0:
                if shard == self.shard_quantity_to or shard == self.shard_quantity:
                    break
                else:
                    continue
            else:
                break
        return result

    def _use_database(self, shard_name, shard_number):
        sql = f"USE {shard_name}_%s"
        self._cur.execute(sql, (shard_number,))


mysql_client = MySQL
