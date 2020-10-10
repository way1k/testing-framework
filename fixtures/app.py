import pytest
from tools.web import select_browser
from tools.web.app import App


@pytest.fixture(scope="function")
def inst_app(driver, cfg):
    app = App(driver, cfg["web"]["url"])
    yield app
    app.close()


@pytest.fixture(scope="function")
def driver(request, cfg):
    browser_type = request.config.getoption("--browser")
    browser = select_browser.local(browser_type)

    browser.set_window_position(2000, 0)  # Для запуска в левом мониторе
    browser.maximize_window()

    yield browser
    browser.quit()
