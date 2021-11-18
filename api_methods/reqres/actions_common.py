import json
import logging
from tools.clients.http import http_client


class Common:

    def __init__(self, base_url):
        self.base_url = base_url
        self.client = http_client(base_url=self.base_url)

    """
    Общие методы
    """

    def api_login_with(self, email, password):
        """
        :param email: почтовый адрес
        :param password: пароль
        """
        response = self.client.post(
            endpoint='/api/login/',
            data={
                "email": email,
                "password": password
            }
        )
        data = json.loads(response.text)
        token = data.get('token')
        assert token is not None, \
            f"Не удалось авторизоваться под пользователем '{email}'"
        logging.info(f"Авторизация под пользователем '{email}'")
        return token

    def api_register(self, email, password):
        """
        :param email: почтовый адрес
        :param password: пароль
        """
        response = self.client.post(
            endpoint='/api/register',
            data={
                "email": email,
                "password": password
            }
        )
        data = json.loads(response.text)
        user_id = data.get('id')
        token = data.get('token')
        assert (token is not None) and (user_id is not None), \
            f"Не удалось зарегистрировать пользователя '{email}'"
        logging.info(f"Регистрация пользователя '{email}'")
        return user_id, token
