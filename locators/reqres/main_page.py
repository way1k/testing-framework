from tools.locator import Locator


class MainPageReqresLocators:

    """
    Локаторы главной страницы
    """

    PAGE = Locator(xpath="/html")
    USER_NOT_FOUND = Locator(xpath="//li[@data-id='users-single-not-found']")
    SINGLE_USER = Locator(xpath="//li[@data-id='users-single']")
    LIST_USERS = Locator(xpath="//li[@data-id='users']")
    URL_IN_REQUEST_BLOCK = Locator(xpath="//strong[contains(text(), 'Request')]/a")