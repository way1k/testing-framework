from pages.bashorg.main_page import MainPageBash
from pages.bashorg.random_page import RandomPageBash
from pages.reqres.main_page import MainPageReqres


class Bashorg:
    """
    Класс-инициализатор для объектов страниц Bashorg
    """

    def __init__(self, browser):
        self.main_page = MainPageBash(browser)
        self.random_page = RandomPageBash(browser)


class Reqres:
    """
    Класс-инициализатор для объектов страниц Reqres
    """

    def __init__(self, browser):
        self.main_page = MainPageReqres(browser)

