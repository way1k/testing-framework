import allure
from pages.page_objects.instagram_profile import ProfileInstPage


class ProfileInstAction(ProfileInstPage):

    @allure.step("Check exist HOME button")
    def check_exist_home_button(self):
        assert self.is_home_button_exist(), "Home button is not exist, login is unsuccessful"

    @allure.step('Search_user')
    def do_search(self, search):
        self.close_save_data_popup()
        self.close_main_popup()
        self.click_search()
        self.input_search_text(search)
        self.select_first_result()

    @allure.step('Like pictures')
    def do_likes(self, quantity_likes):
        self.click_first_picture()
        for _ in range(quantity_likes):
            self.click_like()
            assert self.is_like_exist()
            self.click_unlike()
            assert self.is_unlike_exist()
            self.click_right_arrow()
