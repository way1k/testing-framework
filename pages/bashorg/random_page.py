import time
from pages.base_page import BasePage
from locators.bashorg.random_page import RandomPageBashLocators


class RandomPageBash(BasePage, RandomPageBashLocators):
    """
    Объект страницы случайных цитат
    """

    """
    Методы открытия страницы
    """

    def open_random_page(self):
        self.browser.wd.get(self.browser.bash_url + "/random")
        self.wait_for_ready_state_complete()
        self.browser.asserts.assert_text_on_page("bashorg.org — Лучший Цитатник Рунета")
        self.browser.asserts.assert_url_contains("/random")

    """
    Методы взаимодействия с элементами цитат
    """

    def get_actual_quote_rating(self, quote_number):
        actual_rating = self.find(self._generate_locator_actual_rating(quote_number)).text
        return actual_rating

    def increase_rating(self, quote_number):
        self.smart_click(self._generate_locator_increase_rating(quote_number))

    """
    Методы проверки элементов на странице
    """
    
    def check_upper_block_menu(self):
        self.browser.asserts.assert_element_present(self.UPPER_MENU_BLOCK)

    def check_down_block_menu(self):
        self.browser.asserts.assert_element_present(self.DOWN_MENU_BLOCK)

    def assert_increase_rating(self, rating_before, quote_number):
        time.sleep(1)
        rating_after = self.get_actual_quote_rating(quote_number)
        assert int(rating_before) + 1 == int(rating_after), \
            f"Ожидаемый рейтинг цитаты {int(rating_before) + 1} не равен актуальному {rating_after}"
