# from selenium.webdriver.support.wait import WebDriverWait
# from tools.web.locator import Locator


class App:
    """Web application manager. Wraps driver methods for custom needs."""

    def __init__(self, driver, url, wait=5):
        self.driver = driver
        self.url = url
        # self.wait = WebDriverWait(self.driver, wait).until

    def close(self):
        self.driver.quit()
