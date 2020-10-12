from pages.base_page import BasePage
from tools.web.locator import Locator


class ProfileInstPage(BasePage):
    POPUP_BUTTON = Locator(css='button.HoLwm')
    SAVE_DATA_POPUP = Locator(xpath="//button[contains(text(),'Не сейчас')]")
    HOME_BUTTON = Locator(xpath='//*[local-name()="svg"][@aria-label="Главная страница"]')

    SEARCH_LAYER = Locator(css='span.TqC_a')
    SEARCH = Locator(css='input[placeholder="Поиск"]')
    FIRST_RESULT = Locator(css='.fuqBx > a:first-child')

    FIRST_PICTURE = Locator(css='div.Nnq7C > div:first-child')
    LIKE = Locator(xpath='//*[local-name()="svg"][@aria-label="Нравится"]')
    UNLIKE = Locator(xpath='//*[local-name()="svg"][@aria-label="Не нравится"]')
    RIGHT_ARROW = Locator(css='a.coreSpriteRightPaginationArrow')

    def close_save_data_popup(self):
        self.click_exist_element(self.SAVE_DATA_POPUP)

    def close_main_popup(self):
        self.click_exist_element(self.POPUP_BUTTON)

    def click_search(self):
        self.click(self.SEARCH_LAYER)

    def input_search_text(self, text):
        self.write(self.SEARCH, text)

    def select_first_result(self):
        self.click(self.FIRST_RESULT)

    def click_first_picture(self):
        self.click(self.FIRST_PICTURE)

    def click_like(self):
        self.click(self.LIKE)

    def is_like_exist(self):
        self.is_element_exist(self.LIKE)
        return self

    def click_unlike(self):
        self.click(self.UNLIKE)

    def is_unlike_exist(self):
        self.is_element_exist(self.UNLIKE)
        return self

    def click_right_arrow(self):
        self.click(self.RIGHT_ARROW)

    def is_home_button_exist(self):
        self.is_element_exist(self.HOME_BUTTON)
        return self

