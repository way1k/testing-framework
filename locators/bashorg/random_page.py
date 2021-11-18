from tools.locator import Locator


class RandomPageBashLocators:
    """
    Локаторы страницы рандомных цитат
    """
    PAGE = Locator(xpath="/html")
    UPPER_MENU_BLOCK = Locator(xpath="(//div[@class='menu'])[1]")
    DOWN_MENU_BLOCK = Locator(xpath="(//div[@class='menu'])[2]")

    @staticmethod
    def _generate_locator_actual_rating(quote_number):
        return Locator(xpath=f"(//span[contains(@id, 'result')])[{quote_number}]")

    @staticmethod
    def _generate_locator_increase_rating(quote_number):
        return Locator(xpath=f"(//span[contains(@id, 'result')])[{quote_number}]/preceding-sibling::a")

