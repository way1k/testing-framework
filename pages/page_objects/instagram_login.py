from pages.base_page import BasePage
from tools.web.locator import Locator


class LoginInstPage(BasePage):
    FIELD_LOGIN = Locator(name='username')
    FIELD_PASSWORD = Locator(name='password')
    BUTTON_SUBMIT = Locator(css='button[type="submit"]')

    def open_page(self):
        self.open()

    def write_login(self, login):
        self.write(self.FIELD_LOGIN, login)

    def write_password(self, password):
        self.write(self.FIELD_PASSWORD, password)

    def click_login(self):
        self.click(self.BUTTON_SUBMIT)
