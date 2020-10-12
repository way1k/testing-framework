import allure
from pages.page_objects.yandex_main import YandexMainPage


class YandexMainAction(YandexMainPage):

    @allure.step('Search query')
    def do_search(self, search):
        self.click_search_field()
        self.input_search_query(search)
        self.click_search_button()
