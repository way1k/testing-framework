import json
import logging
from api_methods.reqres.actions_common import Common


class ApiActionsUsers(Common):

    """
    Api методы работы с сервисом пользователей
    """

    def get_user_by_id(self, user_id):
        """
        :param user_id: id пользователя
        """
        response = self.client.get(endpoint=f'/api/users/{user_id}')
        user = json.loads(response.text)
        data = user.get('data')
        support = user.get('support')
        assert (data is not None) and (support is not None), \
            f"Не удалось получить информацию о пользователе user_id:{user_id}"
        logging.info(f"Удалось получить информацию о пользователе user_id:{user_id}")
        return data, support

    def get_list_users_by_page_number(self, page_number):
        """
        :param page_number: номер страницы
        """
        response = self.client.get(endpoint=f'/api/users?page={page_number}')
        users = json.loads(response.text)
        data = users.get('data')
        assert len(data) > 0, \
            f"Не удалось получить информацию о пользователях на странице:{page_number}"
        logging.info(f"Удалось получить информацию о пользователях на странице:{page_number}")
        return users

    def check_email_in_list_of_users(self, users_data, expected_email):
        email = False
        for user in users_data['data']:
            if user['email'] == expected_email:
                email = True
                break
        assert email, f"Почта '{expected_email}' не обнаружена в списке пользователей"
