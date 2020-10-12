from pages.base_page import BasePage
from tools.web.locator import Locator


class YandexMainPage(BasePage):
    SEARCH_FIELD = Locator(xpath="//input[@id='text']")
    SEARCH_BUTTON = Locator(xpath="//div[2]/button[contains(@class, 'utton mini-suggest__button button_theme_websearch button_size_ws-head i-bem button_js_inited')]")

    def open_page(self):
        self.open()

    def input_search_query(self, text):
        self.write(self.SEARCH_FIELD, text)

    def click_search_field(self):
        self.click(self.SEARCH_FIELD)

    def click_search_button(self):
        self.click(self.SEARCH_BUTTON)
