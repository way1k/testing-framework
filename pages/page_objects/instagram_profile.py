import allure
from pages.base_page import BasePage
from tools.web.locator import Locator


class ProfileInstPage(BasePage):
    POPUP_BUTTON = Locator(css='button.HoLwm')

    SEARCH_LAYER = Locator(css='span.TqC_a')
    SEARCH = Locator(css='input[placeholder="Поиск"]')
    FIRST_RESULT = Locator(css='.fuqBx > a:first-child')

    HOME_BUTTON = Locator(xpath='//*[local-name()="svg"][@aria-label="Главная страница"]')

    FIRST_PICTURE = Locator(css='div.Nnq7C > div:first-child')
    LIKE = Locator(css='svg[aria-label="Нравится"]:first-child')
    UNLIKE = Locator(css='svg[aria-label="Не нравится"]')
    RIGHT_ARROW = Locator(css='a.coreSpriteRightPaginationArrow')

    @allure.step('Поиск пользователя')
    def do_search(self, search):
        if self.is_element_exist(self.POPUP_BUTTON):
            self.click(self.POPUP_BUTTON)
        self.click(self.SEARCH_LAYER)
        self.write(self.SEARCH, search)
        self.click(self.FIRST_RESULT)

    @allure.step('Простановка лайков')
    def like(self):
        self.click(self.FIRST_PICTURE)
        self.click(self.LIKE)

    @allure.step('Проверка наличия лайка')
    def is_like_exist(self):
        self.is_element_exist(self.UNLIKE)
        return self

    @allure.step('Снятие лайка')
    def unlike(self):
        self.click(self.UNLIKE)

    @allure.step('Проверка отсутсвия лайка')
    def is_unlike_exist(self):
        self.is_element_exist(self.LIKE)
        return self

    @allure.step('Простановка лайков')
    def likes(self):
        self.click(self.FIRST_PICTURE)
        i = 0
        while i < 20:
            self.click(self.LIKE)
            self.is_like_exist()
            self.click(self.UNLIKE)
            self.is_unlike_exist()
            if i == 18:
                break
            self.click(self.RIGHT_ARROW)
            i += 1

    def is_home_button_exist(self):
        self.is_element_exist(self.HOME_BUTTON)
        return self
