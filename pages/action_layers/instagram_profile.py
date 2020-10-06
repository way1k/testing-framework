import allure
from pages.page_objects.instagram_profile import ProfileInstPage


class ProfileInstAction(ProfileInstPage):

    @allure.step("Check exist HOME button")
    def check_exist_home_button(self):
        assert self.is_home_button_exist(), "Home button is not exist, login is unsuccessful"
