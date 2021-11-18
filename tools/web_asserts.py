import time
from tools.locator import Locator
from pages.base_page import BasePage
from selenium.common.exceptions import ElementNotVisibleException, NoSuchElementException, WebDriverException


class Asserts(BasePage):
    """
    Класс проверок состояний элементов страницы
    """

    """
    Методы проверок текста
    """

    def assert_text_on_page(self, text: str, locator: Locator = Locator(css="html"), timeout=None):
        self.wait_for_ready_state_complete()
        try:
            self.wait_text_visible(text, locator, timeout)
        except WebDriverException as e:
            message = f"Ожидаемый текст '{text}' в локаторе '{locator.value}' не появился по {e}"
            raise AssertionError(message)

    def assert_text_present_on_page(self, text: str, sleep_second: int = None):
        self.wait_for_ready_state_complete()
        if sleep_second:
            time.sleep(sleep_second)
        body_text = self.browser.wd.find_element_by_tag_name('body').text
        try:
            assert text in body_text
        except AssertionError:
            raise AssertionError(f"Текст '{text}' не найден на странице")

    def assert_text_not_on_page(self, text: str, locator: Locator = Locator(css="html")):
        element = self.find(locator)
        assert text not in element.text, \
            f"Текст '{text}' элемента '{locator}' все еще содержится в элементе либо не соответствует ему"

    def assert_text_in_element(self, text: str, locator: Locator):
        element_text = self.find(locator).text
        assert text in element_text, \
            f"Найденный текст '{element_text}' элемента '{locator}' не соответствует искомому '{text}'"

    def assert_text_not_in_element(self, text: str, locator: Locator):
        element_text = self.find(locator).text
        assert text not in element_text, \
            f"Найденный текст '{element_text}' элемента '{locator}' соответствует искомому '{text}'"

    def assert_element_value(self, expected_value: str, locator: Locator):
        element_value = self.get_element_value(locator)
        assert expected_value in element_value, \
            f"Найденное значение элемента '{element_value}' не соответствует искомому '{expected_value}'"

    def assert_element_attribute(self, locator: Locator, expected_value: str, attribute: str):
        element = self.find(locator=locator)
        element_value = element.get_attribute(attribute)
        assert expected_value in element_value, \
            f"Найденное значение элемента '{element_value}' не соответствует искомому '{expected_value}'"

    """
    Методы проверок элементов
    """

    def assert_element_present(self, locator: Locator, timeout=None):
        self.wait_for_ready_state_complete()
        for x in range(3):
            try:
                element = self.wait_present(locator, timeout)
                if element:
                    return True
            except WebDriverException:
                self.browser.wd.refresh()
        raise NoSuchElementException(f"Элемент '{locator}' не найден на странице")

    def assert_element_visible(self, locator: Locator, timeout=None):
        self.wait_for_ready_state_complete()
        for x in range(3):
            try:
                element = self.wait_visible(locator, timeout)
                if element:
                    return True
            except WebDriverException:
                self.browser.wd.refresh()
        raise ElementNotVisibleException(f"Элемент '{locator}' не отображается на странице")

    """
    Методы проверок ссылок
    """

    def assert_url_contains(self, expected_part: str):
        self.wait_for_ready_state_complete()
        assert expected_part in self.browser.wd.current_url

    def assert_url_not_contains(self, expected_part: str):
        self.wait_for_ready_state_complete()
        assert expected_part not in self.browser.wd.current_url

    def assert_tittle_contains(self, expected_title: str):
        self.wait_for_ready_state_complete()
        assert expected_title in self.browser.wd.title, \
            f"Текущий заголовок '{self.browser.wd.title}' не соответствует ожидаемому '{expected_title}'"

    def assert_tittle_not_contains(self, expected_title: str):
        assert expected_title not in self.browser.wd.title, \
            f"Текущий заголовок '{self.browser.wd.title}'  соответствует ожидаемому '{expected_title}'"
