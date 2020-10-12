import pytest
from pages.action_layers.yandex_main import YandexMainAction

QUERY = "Python 3"


@pytest.mark.smoke
def test_search(yandex_app):
    search = YandexMainAction(yandex_app)
    search.open_page()
    search.do_search(QUERY)
