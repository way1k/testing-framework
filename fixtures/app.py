import pytest
from tools.web import select_browser
from tools.web.app import App


@pytest.fixture(scope="function")
def inst_app(driver, cfg):
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

    driver_instance = None

    def get_driver(hub_path=None):
        nonlocal driver_instance
        if is_remote:
            hub_path = hub_path or "http://selenium__standalone-chrome:4444/wd/hub"
            driver = select_browser.remote(browser_type, hub_path)
        else:
            driver = select_browser.local(browser_type)

        driver.set_window_position(2000, 0)
        driver.maximize_window()

        driver_instance = driver

        return driver

    yield get_driver

