from tools.locator import Locator


class MainPageBashLocators:
    """
    Локаторы главной страницы
    """
    PAGE = Locator(xpath="/html")
    UPPER_MENU_BLOCK = Locator(xpath="(//div[@class='menu'])[1]")
    DOWN_MENU_BLOCK = Locator(xpath="(//div[@class='menu'])[2]")

    @staticmethod
    def _generate_locator_type_quotes(quotes_type):
        return Locator(xpath=f"(//div[@class='menu'])[1]/a[contains(text(), '{quotes_type}')]")

