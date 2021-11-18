from tools.clients.http import http_client
from api_methods.reqres.actions_common import Common
from api_methods.reqres.actions_users import ApiActionsUsers


class BackAPI:

    """
    Класс-инициализатор объектов пользователей и генерации пакетов для площадки reqres
    """

    def __init__(self, base_url):
        self.client = http_client(base_url)
        self.actions = Actions(base_url)


class Actions:

    def __init__(self, base_url):
        self.common = Common(base_url)
        self.users = ApiActionsUsers(base_url)
