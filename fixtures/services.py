import pytest

from services.reqres_service.service import ReqresService


@pytest.fixture(scope="function")
def reqres_service():
    yield ReqresService()
