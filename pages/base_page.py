from tools.web.locator import Locator
from selenium.webdriver.support.wait import WebDriverWait
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support import expected_conditions as conditions


class WaitElements:
    """Explicit wait"""

    def __init__(self, app):
        self.app = app

    def wait(self, method, message="", wait_method: str = "until", timeout: float = 10):
        web_driver_wait = WebDriverWait(self.app.driver, timeout)
        wait_func = getattr(web_driver_wait, wait_method, None)
        if wait_func is None:
            raise AttributeError(f"WebDriverWait have no method \"{wait_method}\"")
        return wait_func(method, message)

    def wait_present(self, locator):
        return self.wait(
            method=conditions.presence_of_element_located((locator.by, locator.value))
        )

    def wait_visible(self, locator):
        return self.wait(
            method=conditions.visibility_of_element_located((locator.by, locator.value))
        )

    def wait_clickable(self, locator):
        return self.wait(
            method=conditions.element_to_be_clickable((locator.by, locator.value))
        )


class BasePage(WaitElements):
    """Base Web page object"""
    # def __init__(self, app):
    #     self.app = app

    def find(self, element: Locator):
        """Find element by locator"""
        return self.app.driver.find_element(element.by, element.value)

    def findall(self, element: Locator):
        """Find all elements by locator"""
        return self.app.driver.find_elements(element.by, element.value)

    def open(self):
        """Opens page URL"""
        self.app.driver.get(self.app.url)
        return self

    def goto(self, url):
        """Go to URL"""
        self.app.driver.get(url)

    def click(self, element: Locator):
        """Clicks selected web element"""
        self.wait_clickable(element)
        web_element = self.find(element)
        web_element.click()
        return self

    def write(self, element: Locator, text):
        """Inputs text to selected web element"""
        self.wait_clickable(element)
        field = self.find(element)
        field.click()
        field.clear()
        field.send_keys(text)
        return self

    def is_element_exist(self, element: Locator):
        try:
            self.wait_clickable(element)
            self.find(element)
        except NoSuchElementException:
            return False
        return True

    def click_exist_element(self, element: Locator):
        if self.is_element_exist(element):
            self.click(element)


