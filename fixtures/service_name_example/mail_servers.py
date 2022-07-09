import os

import pytest

from tools.clients.imap import IMAPClient


@pytest.fixture(scope="session")
def mail_server():
    imap = IMAPClient(
        host=os.environ.get("MAIL_SERVER_HOST"),
        username=os.environ.get("MAIL_SERVER_USERNAME"),
        password=os.environ.get("MAIL_SERVER_PASSWORD"),
    )
    yield imap
    imap.logout()
