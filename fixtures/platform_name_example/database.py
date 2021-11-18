import os
import pytest
from tools.clients.mysql import MySQLDataBase


@pytest.fixture(scope="session")
def connection_fixture_example():
    mysql = MySQLDataBase(
        host=os.environ.get("TEST_DATA_HOST"),
        password=os.environ.get("TEST_DATA_PASSWORD"),
        database=os.environ.get("TEST_DATA_BASE"),
        user=os.environ.get("TEST_DATA_USER")
    )
    yield mysql
    mysql.close_connection()
