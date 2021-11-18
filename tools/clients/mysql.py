from pymysql.constants import CLIENT
import pymysql
import logging
import time


class MySQLDataBase:
    """
    Класс клиента подключения к базе данных MySQL
    """

    def __init__(self, host, database, user, password, shard_name=None, shard_quantity=None, shard_quantity_from=None,
                 shard_quantity_to=None):

        self.shard_name = shard_name
        self.shard_quantity = shard_quantity
        self.shard_quantity_from = shard_quantity_from
        self.shard_quantity_to = shard_quantity_to
        self.shard_number = None
        self.connection = pymysql.connect(
            host=host,
            database=database,
            user=user,
            password=password,
            autocommit=True,
            cursorclass=pymysql.cursors.DictCursor,
            connect_timeout=500,
            read_timeout=10,
            write_timeout=10,
            client_flag=CLIENT.MULTI_STATEMENTS)
        self.cursor = self.connection.cursor()

    def query_to_shards(self, query_func, query_func_args=None):
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
            logging.debug(f"Используется шард №{shard}")
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
        self.cursor.execute(sql, (shard_number,))

    def close_connection(self):
        if not self.connection:
            return
        if self.cursor:
            self.cursor.close()
        self.connection.close()

    def execute_query(self, query):
        self.connection.ping()
        query = query if isinstance(query, str) else str(query)
        self.cursor.execute(query)
        logging.debug(f"Выполнен запрос '{query}'")

    def fetchone_result(self, query, wait_retries: int = None, retries_delay=5):
        if wait_retries:
            actual_retries = 0
            while 1:
                self.execute_query(query)
                row = self.cursor.fetchone()
                if actual_retries > 0:
                    logging.debug(f"Повторный запрос №{actual_retries}")
                if row == {} or row == () or row is None:
                    actual_retries += 1
                    if actual_retries == wait_retries:
                        raise AssertionError(f"Запрос возвращает пустой ответ. "
                                             f"Проверьте корректность запроса или подключение к базе. "
                                             f"Запрос '{query}'")
                    time.sleep(retries_delay)
                else:
                    return row
        else:
            self.execute_query(query)
            row = self.cursor.fetchone()
            if not row:
                return {}
            return row

    def fetchall_results(self, query, wait_retries: int = None, retries_delay=5):
        if wait_retries:
            actual_retries = 0
            while 1:
                self.execute_query(query)
                rows = self.cursor.fetchall()
                if actual_retries > 0:
                    logging.debug(f"Повторный запрос №{actual_retries}")
                if (rows == []) or (rows == [{}]) or (rows == ()) or len(rows) == 0:
                    actual_retries += 1
                    if actual_retries == wait_retries:
                        raise AssertionError(f"Запрос возвращает пустой ответ. "
                                             f"Проверьте корректность запроса или подключение к базе. "
                                             f"Запрос '{query}'")
                    time.sleep(retries_delay)
                else:
                    return rows
        else:
            self.execute_query(query)
            rows = self.cursor.fetchall()
            if not rows:
                return {}
            return rows


mysql_client = MySQLDataBase
