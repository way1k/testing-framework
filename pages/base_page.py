import time
from tools.browser import browser_setup
from tools.locator import Locator
from selenium.webdriver import ActionChains
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.common.exceptions import NoSuchElementException, WebDriverException, TimeoutException


class BasePage:
    """
    Общий класс для всех объектов страниц
    """

    def __init__(self, browser: 'browser_setup.Browser'):
        self.browser = browser
        self.timeout = 20
        self.action_chains = ActionChains(self.browser.wd)

    """
    Методы поиска элемента
    """

    def find(self, locator: Locator, timeout: int = None):
        self.wait_for_ready_state_complete()
        try:
            return self.wait_present(locator, timeout)
        except TimeoutException:
            raise NoSuchElementException(f"Не удалось найти локатор '{locator}'")

    def find_all(self, locator: Locator):
        self.wait_for_ready_state_complete()
        try:
            return self.browser.wd.find_elements(locator.by, locator.value)
        except NoSuchElementException:
            raise NoSuchElementException(f"Не удалось найти локаторы '{locator}'")

    """
    Методы наведения и клика на элемент
    """

    def hover_on_element(self, element):
        self.action_chains.move_to_element(element).perform()
        return element

    def hover_on_element_located(self, locator: Locator):
        self.wait_for_ready_state_complete()
        element = self.find(locator)
        self.action_chains.move_to_element(element).perform()
        return element

    def click_by_property(self, locator: Locator):
        self.browser.wd.execute_script("arguments[0].click();", self.find(locator=locator))

    def smart_click(self, locator: Locator, timeout=None, retries=2):
        for n in range(retries):
            try:
                web_element = self.wait_clickable(locator=locator, timeout=timeout)
                return web_element.click()
            except WebDriverException as e:
                time.sleep(1)
                if n == retries - 1:
                    raise WebDriverException(f"Не удается найти элемент '{locator.value}' по: {e}")
                else:
                    continue

    def smart_action(self, locator: Locator, action: str, retries: int = 2, *args, **kwargs):
        for n in range(retries):
            try:
                web_element = self.wait_present(
                    locator=locator,
                    message=f"Не удалось найти '{locator.value}' на странице '{self.browser.wd.current_url}'"
                )
                action_method = getattr(web_element, action, None)
                if not action_method:
                    raise Exception(f"Веб элемент не содержит действие '{action}'")
                return action_method(*args, **kwargs)
            except Exception as e:
                time.sleep(1)
                if n == retries - 1:
                    raise Exception(f"Не удалось выполнить '{action}' для локатора '{locator.value}': {e}")
                else:
                    continue

    """
    Методы заполнения полей
    """

    def fill_form(self, locator: Locator, text: str, click_before: bool = True):
        element = self.find(locator)
        if click_before:
            element.click()
        element.clear()
        element.send_keys(text)

    def fill_form_value(self, field_name: str, text:  str or int):
        self.find(locator=Locator(name=f"{field_name}")).click()
        self.find(locator=Locator(name=f"{field_name}")).clear()
        self.find(locator=Locator(name=f"{field_name}")).send_keys(text)

    """
    Методы выбора значения из выпадающего списка
    """

    def select_value(self, select_locator: Locator, value: str, attribute: str = "text"):
        if value:
            element_select = self.find(select_locator)
            all_options = element_select.find_elements_by_tag_name("option")
            for option in all_options:
                if value in option.get_attribute(attribute):
                    option.click()
                    break

    """
    Методы получения свойств элемента
    """

    def get_element_attribute(self, locator: Locator, attribute: str, timeout: int = None):
        element = self.find(locator=locator, timeout=timeout)
        return element.get_attribute(attribute)

    def get_element_value(self, locator: Locator, timeout: int = None):
        element = self.find(locator=locator, timeout=timeout)
        return element.get_attribute("value")

    def get_element_text(self, locator: Locator, timeout: int = None):
        element = self.find(locator=locator, timeout=timeout)
        return element.get_attribute("text")

    """
    Методы получения свойств элементов через querySelector
    """

    def get_document_query_shadow_element(self, locator: Locator):
        return self.browser.wd.execute_script(f"return document.querySelector('{locator.value}').shadowRoot")

    def get_document_query_option_value(self, locator: Locator):
        return self.browser.wd.execute_script(f"return document.querySelector('{locator.value} option:checked').value")

    """
    Методы проверки состояния элемента
    """

    def is_checkbox_checked(self, locator: Locator):
        return bool(self.get_element_attribute(locator=locator, attribute='checked'))

    def is_element_present(self, locator: Locator):
        try:
            self.find(locator=locator, timeout=3)
            return True
        except WebDriverException:
            return False

    def is_element_visible(self, locator: Locator):
        try:
            element = self.find(locator)
            return element.is_displayed()
        except WebDriverException:
            return False

    """
    Методы ожидания
    """

    def __wait(self, method, message="", wait_method: str = "until", timeout: float = None):
        if not timeout:
            timeout = self.timeout
        web_driver_wait = WebDriverWait(self.browser.wd, timeout)
        wait_func = getattr(web_driver_wait, wait_method, None)
        if wait_func is None:
            raise AttributeError(f"Вебдрайвер не содержит метода '{wait_method}'")
        return wait_func(method, message)

    def wait_present(self, locator: Locator, timeout: int = None, message: str = None):
        if not message:
            message = f"Элемент '{locator}' не появился на странице"
        return self.__wait(
            method=ec.presence_of_element_located((locator.by, locator.value)),
            message=message,
            timeout=timeout
        )

    def wait_visible(self, locator: Locator, timeout: int = None, message: str = None):
        if not message:
            message = f"Элемент '{locator}' не стал видимым на странице"
        return self.__wait(
            method=ec.visibility_of_element_located((locator.by, locator.value)),
            message=message,
            timeout=timeout
        )

    def wait_not_visible(self, locator: Locator, timeout: int = None, message: str = None):
        if not message:
            message = f"Элемент '{locator}' не исчез со страницы"
        return self.__wait(
            method=ec.invisibility_of_element_located((locator.by, locator.value)),
            message=message,
            timeout=timeout
        )

    def wait_clickable(self, locator: Locator, timeout: int = None, message: str = None):
        if not message:
            message = f"Элемент '{locator}' не стал кликабельным"
        return self.__wait(
            method=ec.element_to_be_clickable((locator.by, locator.value)),
            message=message,
            timeout=timeout
        )

    def wait_for_ready_state_complete(self, timeout: int = None):
        return self.__wait(
            method=lambda driver: driver.execute_script('return document.readyState') == 'complete',
            timeout=timeout,
            message=f"Страницу {self.browser.wd.current_url} не удалось загрузить"
        )

    """
    Методы ожидания элемента
    """

    def wait_text_visible(self, text: str, locator: Locator, timeout: int = None, retries: int = 3):
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
                    raise WebDriverException(f"Не удается найти элемент '{locator.value}' по: {e}")
                continue
        if not element:
            raise WebDriverException(f"Не удается найти элемент '{locator.value}'")

    def wait_text_present_on_element(self, locator: Locator, text: str, retry=5, delay=1):
        for _ in range(retry):
            try:
                self.wait_for_ready_state_complete()
                element_text = self.find(locator).text
                assert text in element_text
                return
            except AssertionError:
                if _ == (retry - 1):
                    raise AssertionError(f"Текст '{text}' не найден на странице спустя {retry} обновлений страницы")
                self.browser.wd.refresh()
                time.sleep(delay)
                continue

    """
    Методы работы с таблицами
    """

    def get_table_row(self, table_header: Locator, table_rows: Locator, number_row=1, remove_empty: bool = False):
        """
        Метод получения определенной строки из таблицы на странице
        """
        self.wait_clickable(table_header)
        headers = [value.text for value in self.find_all(table_header)]
        self.wait_clickable(table_rows)
        row = self.find_all(table_rows)[number_row - 1]
        row_values = [value.text for value in row.find_elements_by_xpath('./td')]
        if remove_empty:
            row_values = list(filter(None, row_values))
        return dict(zip(headers, row_values))

    def get_table_value_by_column_name(self,
                                       row_number: str or int,
                                       table_header: Locator,
                                       table_rows: Locator,
                                       column_name: str,
                                       remove_empty: bool = False):
        """
        Метод получения значения ячейки по имени из нужной строки в таблице
        """
        row = self.get_table_row(
            number_row=row_number,
            table_header=table_header,
            table_rows=table_rows,
            remove_empty=remove_empty)
        value = row.get(column_name)
        assert value is not None, f"Значение колонки '{column_name}' пустое или такой колонки в таблице нет"
        return value

    def get_full_table(self, table_header: Locator, table_rows: Locator, remove_empty: bool = False,
                       remove_empty_rows: bool = False):
        """
        Метод получения всех строк таблицы на странице
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
    Методы загрузки файлов
    """

    def download_file_by_click(self, locator):
        self.smart_click(locator)
        self.browser.browser_methods.wait_for_download()
