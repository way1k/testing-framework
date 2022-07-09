from locators.bashorg.main_page import MainPageBashLocators
from pages.base_page import BasePage


class MainPageBash(BasePage, MainPageBashLocators):
    """
    Main page object
    """

    """
    Open page methods
    """

    def open_main_page(self):
        self.browser.wd.get(self.browser.bash_url)
        self.wait_for_ready_state_complete()
        self.browser.asserts.assert_text_on_page("bashorg.org — Лучший Цитатник Рунета")

    """
    Interaction with upper block menu methods
    """

    def select_type_quotes_in_upper_block(self, quotes_type: str = "случайные"):
        self.smart_click(self._generate_locator_type_quotes(quotes_type))

    """
    Check elements at page methods
    """

    def check_upper_block_menu(self):
        self.browser.asserts.assert_element_present(self.UPPER_MENU_BLOCK)

    def check_down_block_menu(self):
        self.browser.asserts.assert_element_present(self.DOWN_MENU_BLOCK)
