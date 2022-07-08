import time
from typing import Callable, Any, Literal

from selenium.webdriver.remote.webelement import WebElement

from tools.browser import browser_setup
from tools.locator import Locator
from selenium.webdriver import ActionChains
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.common.exceptions import NoSuchElementException, WebDriverException, TimeoutException


class BasePage:
    """
    Base class
    """

    def __init__(self, browser: 'browser_setup.Browser') -> None:
        self.browser = browser
        self.timeout = 20
        self.action_chains = ActionChains(self.browser.wd)

    """
    Find methods
    """

    def find(self, locator: Locator, timeout: int | None = None) -> WebElement:
        self.wait_for_ready_state_complete()
        try:
            return self.wait_present(locator, timeout)
        except TimeoutException:
            raise NoSuchElementException(f"Element not found with locator: '{locator}'")

    def find_all(self, locator: Locator) -> list[WebElement]:
        self.wait_for_ready_state_complete()
        try:
            return self.browser.wd.find_elements(locator.by, locator.value)
        except NoSuchElementException:
            raise NoSuchElementException(f"Elements not found with locator: '{locator}'")

    """
    Click and hover methods
    """

    def hover_on_element(self, element: WebElement) -> None:
        self.action_chains.move_to_element(element).perform()

    def hover_on_element_located(self, locator: Locator) -> WebElement:
        self.wait_for_ready_state_complete()
        element = self.find(locator)
        self.action_chains.move_to_element(element).perform()
        return element

    def click_by_property(self, locator: Locator) -> None:
        self.browser.wd.execute_script("arguments[0].click();", self.find(locator=locator))

    def smart_click(self, locator: Locator, timeout: int | None = None, retries: int = 2) -> None:
        for n in range(retries):
            try:
                web_element = self.wait_clickable(locator=locator, timeout=timeout)
                return web_element.click()
            except WebDriverException as e:
                time.sleep(1)
                if n == retries - 1:
                    raise WebDriverException(f"Can't find the element: '{locator.value}'. Error: {e}")
                else:
                    continue

    def smart_action(self, locator: Locator, action: str, retries: int = 2, *args, **kwargs) -> Callable[[Any], Any]:
        for n in range(retries):
            try:
                web_element = self.wait_present(
                    locator=locator,
                    message=f"Can't find the element '{locator.value}' at the page '{self.browser.wd.current_url}'"
                )
                action_method = getattr(web_element, action, None)
                if not action_method:
                    raise Exception(f"WebElement hasn't action: '{action}'")
                return action_method(*args, **kwargs)
            except Exception as e:
                time.sleep(1)
                if n == retries - 1:
                    raise Exception(f"Failed to perform '{action}' for locator '{locator.value}'. Error: {e}")
                else:
                    continue

    """
    Fill forms
    """

    def fill_form(self, locator: Locator, text: str, click_before: bool = True) -> None:
        element = self.find(locator)
        if click_before:
            element.click()
        element.clear()
        element.send_keys(text)

    def fill_form_value(self, field_name: str, text: str | int) -> None:
        self.find(locator=Locator(name=f"{field_name}")).click()
        self.find(locator=Locator(name=f"{field_name}")).clear()
        self.find(locator=Locator(name=f"{field_name}")).send_keys(text)

    """
    Select some values
    """

    def select_value(self, select_locator: Locator, value: str, attribute: str = "text") -> None:
        if value:
            element_select = self.find(select_locator)
            all_options = element_select.find_elements_by_tag_name("option")
            for option in all_options:
                if value in option.get_attribute(attribute):
                    option.click()
                    break

    """
    Working with element attributes
    """

    def get_element_attribute(self, locator: Locator, attribute: str, timeout: int | None = None) -> str:
        element = self.find(locator=locator, timeout=timeout)
        return element.get_attribute(attribute)

    def get_element_value(self, locator: Locator, timeout: int | None = None) -> str:
        element = self.find(locator=locator, timeout=timeout)
        return element.get_attribute("value")

    def get_element_text(self, locator: Locator, timeout: int | None = None) -> str:
        element = self.find(locator=locator, timeout=timeout)
        return element.get_attribute("text")

    """
    Working with element attributes by querySelector
    """

    def get_document_query_shadow_element(self, locator: Locator) -> None:
        return self.browser.wd.execute_script(f"return document.querySelector('{locator.value}').shadowRoot")

    def get_document_query_option_value(self, locator: Locator) -> None:
        return self.browser.wd.execute_script(f"return document.querySelector('{locator.value} option:checked').value")

    """
    Check methods
    """

    def is_checkbox_checked(self, locator: Locator) -> bool:
        return bool(self.get_element_attribute(locator=locator, attribute='checked'))

    def is_element_present(self, locator: Locator) -> bool:
        try:
            self.find(locator=locator, timeout=3)
            return True
        except WebDriverException:
            return False

    def is_element_visible(self, locator: Locator) -> bool:
        try:
            element = self.find(locator)
            return element.is_displayed()
        except WebDriverException:
            return False

    """
    Waiting methods
    """

    def __wait(
            self,
            method: Callable[[tuple | list], WebElement],
            message: str = "",
            wait_method: Literal["until", "until_not"] = "until",
            timeout: int | None = None
    ) -> WebElement:
        if not timeout:
            timeout = self.timeout
        web_driver_wait = WebDriverWait(self.browser.wd, timeout)
        wait_func = getattr(web_driver_wait, wait_method, None)
        if wait_func is None:
            raise AttributeError(f"Webdriver has not the method: '{wait_method}'")
        return wait_func(method, message)

    def wait_present(self, locator: Locator, timeout: int | None = None, message: str | None = None) -> WebElement:
        if not message:
            message = f"Element '{locator}' is not present at the page"
        return self.__wait(
            method=ec.presence_of_element_located((locator.by, locator.value)),
            message=message,
            timeout=timeout
        )

    def wait_visible(self, locator: Locator, timeout: int | None = None, message: str | None = None) -> WebElement:
        if not message:
            message = f"Element '{locator}' is not visible at the page"
        return self.__wait(
            method=ec.visibility_of_element_located((locator.by, locator.value)),
            message=message,
            timeout=timeout
        )

    def wait_not_visible(self, locator: Locator, timeout: int | None = None, message: str | None = None) -> WebElement:
        if not message:
            message = f"Element '{locator}' don't not visible at the page"
        return self.__wait(
            method=ec.invisibility_of_element_located((locator.by, locator.value)),
            message=message,
            timeout=timeout
        )

    def wait_clickable(self, locator: Locator, timeout: int | None = None, message: str | None = None) -> WebElement:
        if not message:
            message = f"Element '{locator}' is not clickable"
        return self.__wait(
            method=ec.element_to_be_clickable((locator.by, locator.value)),
            message=message,
            timeout=timeout
        )

    def wait_for_ready_state_complete(self, timeout: int | None = None) -> WebElement:
        return self.__wait(
            method=lambda driver: driver.execute_script('return document.readyState') == 'complete',
            timeout=timeout,
            message=f"The '{self.browser.wd.current_url}' page could not be loaded"
        )

    """
    Waiting text in element
    """

    def wait_text_visible(
            self,
            text: str,
            locator: Locator,
            timeout: int | None = None,
            retries: int = 3
    ) -> WebElement:
        element = None
        for _ in range(retries):
            try:
                element = self.find(locator, timeout)
                if element.is_displayed() and text in element.text:
                    return element
            except WebDriverException as e:
                if _ == 1:
                    self.browser.wd.refresh()
                if _ == retries - 1:
                    raise WebDriverException(f"Can't find the element '{locator.value}'. Error: {e}")
                continue
        if not element:
            raise WebDriverException(f"Can't find the element '{locator.value}'")

    def wait_text_present_on_element(self, locator: Locator, text: str, retry: int = 5, delay: int = 1) -> None:
        for _ in range(retry):
            try:
                self.wait_for_ready_state_complete()
                element_text = self.find(locator).text
                assert text in element_text
                return
            except AssertionError:
                if _ == (retry - 1):
                    raise AssertionError(f"Text '{text}' was not found on the page after {retry} page updates")
                self.browser.wd.refresh()
                time.sleep(delay)
                continue

    """
    Working with tables
    """

    def get_table_row(
            self,
            table_header: Locator,
            table_rows: Locator,
            number_row: int = 1,
            remove_empty: bool = False
    ) -> dict[str, str]:
        """
        Get row from table
        """
        self.wait_clickable(table_header)
        headers = [value.text for value in self.find_all(table_header)]
        self.wait_clickable(table_rows)
        row = self.find_all(table_rows)[number_row - 1]
        row_values = [value.text for value in row.find_elements_by_xpath('./td')]
        if remove_empty:
            row_values = list(filter(None, row_values))
        return dict(zip(headers, row_values))

    def get_table_value_by_column_name(
            self,
            row_number: str | int,
            table_header: Locator,
            table_rows: Locator,
            column_name: str,
            remove_empty: bool = False
    ) -> str:
        """
        Get data by row number and column name
        """
        row = self.get_table_row(
            number_row=row_number,
            table_header=table_header,
            table_rows=table_rows,
            remove_empty=remove_empty)
        value = row.get(column_name)
        assert value is not None, f"Value of column '{column_name}' is empty or there is no such column in the table"
        return value

    def get_full_table(self, table_header: Locator, table_rows: Locator, remove_empty: bool = False,
                       remove_empty_rows: bool = False) -> list:
        """
        Get all rows in table
        """
        table_info = list()
        quantity_rows = len(self.find_all(table_rows))
        for row in range(1, quantity_rows + 1):
            row_info = self.get_table_row(
                table_header=table_header,
                table_rows=table_rows,
                number_row=row,
                remove_empty=remove_empty
            )
            if remove_empty_rows:
                if len(row_info) == 0:
                    continue
            table_info.append(row_info)
        return table_info

    """
    Download files 
    """

    def download_file_by_click(self, locator: Locator) -> None:
        self.smart_click(locator)
        self.browser.browser_methods.wait_for_download()
