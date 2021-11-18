import os
import pytest
from tools.clients.imap import IMAPClient
from tools.clients.graylog.graylog import GraylogClient


@pytest.fixture(scope="session")
def mail_server():
    imap = IMAPClient(
        host=os.environ.get("MAIL_SERVER_HOST"),
        username=os.environ.get("MAIL_SERVER_USERNAME"),
        password=os.environ.get("MAIL_SERVER_PASSWORD"),
    )
    yield imap
    imap.logout()


@pytest.fixture(scope="session")
def graylog():
    graylog = GraylogClient(
        host=os.environ.get("GRAYLOG_SERVER_HOST"),
        access_token=os.environ.get("GRAYLOG_SERVER_TOKEN"))
    yield graylog
