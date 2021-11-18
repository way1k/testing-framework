from hamcrest import assert_that, is_not, empty
from .endpoints import endpoints
from datetime import datetime
import requests
import json


class GraylogClient:
    """
    Класс-клиента Graylog
    """

    def __init__(self, host: str, access_token: str):
        self._access_token = (access_token, "token")
        self._headers = {'Accept': 'application/json'}
        self.host = host
        self.methods = {
            "get": self._get,
            "post": self._post,
            "put": self._put,
            "delete": self._delete
        }

    def _get(self, endpoint, **kwargs):
        return requests.get(self.host + endpoint, auth=self._access_token, headers=self._headers, params=kwargs)

    def _post(self, endpoint, data, **kwargs):
        return requests.post(self.host + endpoint, auth=self._access_token, headers=self._headers, data=data,
                             params=kwargs)

    def _put(self, endpoint, data, **kwargs):
        return requests.put(self.host + endpoint, auth=self._access_token, headers=self._headers, data=data,
                            params=kwargs)

    def _delete(self, endpoint, data, **kwargs):
        return requests.delete(self.host + endpoint, auth=self._access_token, headers=self._headers, data=data,
                               params=kwargs)

    def fetch_results(self, endpoint, method='get', **kwargs):
        arg_names = kwargs.keys()
        required_args = endpoints[endpoint]
        if not set(required_args).issubset(set(arg_names)):
            raise ValueError(('Не все обязательные аргументы были переданы %s.\n' +
                              'Передано: %s\nТребуется: %s')
                             % (endpoint, arg_names, required_args))
        for arg in required_args:
            if arg in kwargs and arg[-1] == '_':
                kwargs[arg[:-1]] = kwargs.pop(arg)
        return self.methods[method](endpoint=endpoint, **kwargs)

    def get_last_messages_by_query(self, query, fields='message, source', date_from=None, date_to=None):
        if not date_from:
            date_from = datetime.today().strftime('%Y-%m-%d 00:00:00')
        if not date_to:
            date_to = datetime.today().strftime('%Y-%m-%d 23:59:59')
        request_params = {
            "query": f"{query}",
            "fields": f"{fields}",
            "from": f"{date_from}",
            "to": f"{date_to}",
        }

        response = self.fetch_results(endpoint="/api/search/universal/absolute", **request_params)
        result_json = json.loads(json.dumps(response.json(), ensure_ascii=False, indent=None, sort_keys=True))
        assert_that(result_json["messages"], is_not(empty()))
        return result_json["messages"]

    @staticmethod
    def check_message_field_text(messages, message_field, expected_text):
        messages_list = []
        for message_log in messages:
            if message_field in message_log['message']:
                messages_list.append(message_log['message'][message_field])
        assert any(
            expected_text in text for text in messages_list), f"Сообщение {expected_text} не обнаружено в Graylog"
