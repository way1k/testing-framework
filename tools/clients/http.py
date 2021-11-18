from urllib.parse import urlparse
import requests
import logging
import allure
import time


class HTTPMethods:
    """
    Класс http-клиента
    """

    def __init__(self, base_url, session=requests.session()):
        self.base_url = base_url
        self.session = session

    def __perform_request(self, func, endpoint, retries=5, data=None, json=None, headers=None, rpc=False,
                          return_session=False, not_valid=None, fake_post=False, expected_code=None,
                          request_data=False, files=None, **kwargs):

        login_session = self.session

        if fake_post:
            self.base_url = "http://localhost:5000"

        for _ in range(retries):

            response = self.session.request(
                method=func,
                url=self.base_url + self.__format_url(endpoint) if not rpc else endpoint,
                data=data,
                json=json,
                headers=headers,
                files=files,
                verify=False,
                **kwargs
            )
            self.__request_log(func, response, data, request_data)

            if not_valid:
                return response
            else:
                retry_status_code_list = [403, 404, 500, 501, 502, 503, 504]
                if response.status_code != expected_code and response.status_code not in retry_status_code_list:
                    self.__allure_html(response.text)
                    raise AssertionError(
                        f"Ожидаемый статус-код [{expected_code}] не равен актуальному [{response.status_code}]")
                elif response.status_code in retry_status_code_list:
                    if _ == retries - 1:
                        self.__allure_html(response.text)
                        raise AssertionError(
                            f"Ожидаемый статус-код [{expected_code}] не равен актуальному [{response.status_code}]")
                    time.sleep(2)
                    continue
                else:
                    break
        if return_session:
            return login_session
        else:
            return response

    @staticmethod
    def __request_log(func, response, data=None, request_data=False):
        logging.debug(f'{func.upper()}[{response.status_code}]: {response.url}')

        if request_data and data:
            logging.debug(f"Данные запроса: {data}")

    @staticmethod
    def __allure_html(data):
        allure.attach(data, name='HTML Attachment', attachment_type=allure.attachment_type.HTML)

    def get(self, endpoint, return_session=False, not_valid=None, expected_code=200, **kwargs):
        response = self.__perform_request(
            func="get",
            endpoint=endpoint,
            not_valid=not_valid,
            expected_code=expected_code,
            return_session=return_session,
            **kwargs
        )

        return response

    def post(self, endpoint, data=None, json=None, headers=None, rpc=False, return_session=False, not_valid=None,
             fake_post=False, expected_code=200, request_data=False, files=None, **kwargs):
        response = self.__perform_request(
            func="post",
            endpoint=endpoint,
            rpc=rpc,
            headers=headers,
            data=data,
            json=json,
            files=files,
            not_valid=not_valid,
            fake_post=fake_post,
            request_data=request_data,
            expected_code=expected_code,
            return_session=return_session,
            **kwargs
        )

        return response

    def put(self, endpoint, data=None, headers=None, expected_code=200, **kwargs):
        response = self.__perform_request(
            func="put",
            endpoint=endpoint,
            headers=headers,
            data=data,
            expected_code=expected_code,
            **kwargs
        )

        return response

    def delete(self, endpoint, data=None, headers=None, expected_code=200, **kwargs):
        response = self.__perform_request(
            func="delete",
            endpoint=endpoint,
            headers=headers,
            data=data,
            expected_code=expected_code,
            **kwargs
        )

        return response

    def __format_url(self, url):
        if self.base_url in url:
            format_url = urlparse(url).path
        else:
            return url
        return format_url

    def close_session(self):
        self.session.close()

    def clear_cookies(self):
        self.session.cookies.clear()


http_client = HTTPMethods
