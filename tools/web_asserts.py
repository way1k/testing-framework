import time

from selenium.common.exceptions import WebDriverException

from pages.base_page import BasePage
from tools.locator import Locator


class WebAsserts(BasePage):
    """
    Web asserts
    """

    """
    Assert texts
    """

    def assert_text_on_page(
        self, text: str, locator: Locator = Locator(css="html"), timeout: int | None = None
    ) -> None:
        self.wait_for_ready_state_complete()
        try:
            self.wait_text_visible(text, locator, timeout)
        except WebDriverException as e:
            message = f"Expected text '{text}' not present in locator '{locator.value}'. Error: {e}"
            raise AssertionError(message)

    def assert_text_present_on_page(self, text: str, sleep_second: int = None) -> None:
        self.wait_for_ready_state_complete()
        if sleep_second:
            time.sleep(sleep_second)
        body_text = self.browser.wd.find_element_by_tag_name("body").text
        try:
            assert text in body_text
        except AssertionError:
            raise AssertionError(f"Text '{text}' not found at the page")

    def assert_text_not_on_page(self, text: str, locator: Locator = Locator(css="html")) -> None:
        element = self.find(locator)
        assert (
            text not in element.text
        ), f"Text '{text}' in WebElement '{locator}' is still contained in the element or does not correspond to it"

    def assert_text_in_element(self, text: str, locator: Locator) -> None:
        element_text = self.find(locator).text
        assert (
            text in element_text
        ), f"Found text '{element_text}' in WebElement '{locator}' doesn't match to expected text '{text}'"

    def assert_text_not_in_element(self, text: str, locator: Locator) -> None:
        element_text = self.find(locator).text
        assert (
            text not in element_text
        ), f"Found text '{element_text}' in WebElement '{locator}' match to expected text '{text}'"

    def assert_element_value(self, expected_value: str, locator: Locator) -> None:
        element_value = self.get_element_value(locator)
        assert (
            expected_value in element_value
        ), f"Found WebElement value '{element_value}' doesn't match to expected '{expected_value}'"

    def assert_element_attribute(self, locator: Locator, expected_value: str, attribute: str) -> None:
        element = self.find(locator=locator)
        element_value = element.get_attribute(attribute)
        assert (
            expected_value in element_value
        ), f"Found WebElement attribute '{element_value}' doesn't match to expected '{expected_value}'"

    """
    Assert link
    """

    def assert_url_contains(self, expected_part: str):
        self.wait_for_ready_state_complete()
        assert expected_part in self.browser.wd.current_url

    def assert_url_not_contains(self, expected_part: str):
        self.wait_for_ready_state_complete()
        assert expected_part not in self.browser.wd.current_url

    def assert_tittle_contains(self, expected_title: str):
        self.wait_for_ready_state_complete()
        assert (
            expected_title in self.browser.wd.title
        ), f"Current title '{self.browser.wd.title}' does not match to expected '{expected_title}'"

    def assert_tittle_not_contains(self, expected_title: str):
        assert (
            expected_title not in self.browser.wd.title
        ), f"Current title '{self.browser.wd.title}' does not match to expected '{expected_title}'"
