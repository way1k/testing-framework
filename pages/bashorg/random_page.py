import time

from locators.bashorg.random_page import RandomPageBashLocators
from pages.base_page import BasePage


class RandomPageBash(BasePage, RandomPageBashLocators):
    """
    Page object for random quotes page
    """

    """
    Open page methods
    """

    def open_random_page(self):
        self.browser.wd.get(self.browser.bash_url + "/random")
        self.wait_for_ready_state_complete()
        self.browser.asserts.assert_text_on_page("bashorg.org — Лучший Цитатник Рунета")
        self.browser.asserts.assert_url_contains("/random")

    """
    Interactions with quote elements methods
    """

    def get_actual_quote_rating(self, quote_number):
        actual_rating = self.find(self._generate_locator_actual_rating(quote_number)).text
        return actual_rating

    def increase_rating(self, quote_number):
        self.smart_click(self._generate_locator_increase_rating(quote_number))

    """
    Methods for checking elements on a page
    """

    def check_upper_block_menu(self):
        self.browser.asserts.assert_element_present(self.UPPER_MENU_BLOCK)

    def check_down_block_menu(self):
        self.browser.asserts.assert_element_present(self.DOWN_MENU_BLOCK)

    def assert_increase_rating(self, rating_before, quote_number):
        time.sleep(1)
        rating_after = self.get_actual_quote_rating(quote_number)
        assert int(rating_before) + 1 == int(
            rating_after
        ), f"Expected rating of quote {int(rating_before) + 1} not equal current {rating_after}"
