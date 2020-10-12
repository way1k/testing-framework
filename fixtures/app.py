import pytest
from tools.web import select_browser
from tools.web.app import App


@pytest.fixture(scope="function")
def inst_app(driver, cfg):
    app = App(driver, cfg["web"]["url"])
    yield app
    app.close()


@pytest.fixture(scope="function")
def yandex_app(driver, cfg):
    app = App(driver, cfg["web"]["url"])
    yield app
    app.close()


# @pytest.fixture(scope="function")
# def driver(request, cfg):
#     browser_type = request.config.getoption("--browser")
#     browser = select_browser.local(browser_type)
#
#     browser.set_window_position(2000, 0)  # Для запуска в левом мониторе
#     browser.maximize_window()
#
#     yield browser
#     browser.quit()


@pytest.fixture(scope="function")
def driver(request, cfg):
    is_remote = request.config.getoption("--remote")
    browser_type = request.config.getoption("--browser")

    if is_remote:
        hub_path = "http://selenium__standalone-chrome:4444/wd/hub"
        browser = select_browser.remote(browser_type, hub_path)
    else:
        browser = select_browser.local(browser_type)

    browser.set_window_position(2000, 0)
    browser.maximize_window()

    yield browser
    browser.quit()


