import allure
from pages.page_objects.instagram_login import LoginInstPage


class LoginInstAction(LoginInstPage):

    @allure.step("Login Instagram")
    def do_login(self, login, password):
        self.open()
        self.write_login(login)
        self.write_password(password)
        self.click_login()
