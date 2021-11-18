from locators.reqres.main_page import MainPageReqresLocators
from pages.base_page import BasePage


class MainPageReqres(BasePage, MainPageReqresLocators):
    """
    Объект главной страницы REQRES
    """

    """
    Методы открытия страницы
    """

    def open_main_page(self):
        self.browser.wd.get(self.browser.reqres_url)
        self.wait_for_ready_state_complete()
        self.browser.asserts.assert_text_on_page("Test your front-end against a real API")

    """
    Методы взаимодействия с блоком запросов
    """

    def click_button_user_not_found(self):
        self.smart_click(self.USER_NOT_FOUND)

    def click_button_single_user(self):
        self.smart_click(self.SINGLE_USER)

    def click_button_list_users(self):
        self.smart_click(self.LIST_USERS)

    """
    Методы проверки элементов на странице
    """

    def check_url_in_request_block(self, expected_url: str):
        actual_url = self.get_element_attribute(
            locator=self.URL_IN_REQUEST_BLOCK,
            attribute="href"
        )
        assert actual_url == (self.browser.reqres_url + expected_url), \
            f"Ожидаемый url {self.browser.reqres_url + expected_url}, не равен актуальному {actual_url}"
