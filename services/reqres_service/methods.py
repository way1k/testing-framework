from services.reqres_service.endpoints import ReqresEndpoints
from tools.response_validate import ResponseValidate


class ReqresMethods(ReqresEndpoints):
    """reqres service methods"""

    def method_get_user_by_id(self, user_id: int, expected_status_code: int = 200) -> ResponseValidate:
        """
        Get user by user_id

        :param user_id: User id
        :param expected_status_code: Expected status code in response
        """

        r = self.get_api_users(source_url_params={"user_id": user_id})
        r.assert_status_code(expected_status_code)
        return r

    def method_api_login_with(
        self, email: str | None = None, password: str | None = None, expected_status_code: int = 200
    ) -> ResponseValidate:
        """
        Login by email & password

        :param email: Email
        :param password: Password
        :param expected_status_code: Expected status code in response
        """

        json_data = dict()
        args = locals()
        for key in list(args):
            if key not in ("args", "json_data", "self", "expected_status_code"):
                json_data = json_data | {key: args[key]} if (args[key] or args[key] in (0, [], "")) else json_data
        r = self.post_api_login(json=json_data)
        r.assert_status_code(expected_status_code)
        return r

    def method_api_register(
        self, email: str | None = None, password: str | None = None, expected_status_code: int = 200
    ) -> ResponseValidate:
        """
        Register new user

        :param email: Email
        :param password: Password
        :param expected_status_code: Expected status code in response
        """

        json_data = dict()
        args = locals()
        for key in list(args):
            if key not in ("args", "json_data", "self", "expected_status_code"):
                json_data = json_data | {key: args[key]} if (args[key] or args[key] in (0, [], "")) else json_data
        r = self.post_api_register(json=json_data)
        r.assert_status_code(expected_status_code)
        return r

    def method_get_list_users(self, page: str | None = None, expected_status_code: int = 200) -> ResponseValidate:
        """
        :param page: Page number
        :param expected_status_code: Expected status code in response
        """

        json_data = dict()
        args = locals()
        for key in list(args):
            if key not in ("args", "json_data", "self", "expected_status_code"):
                json_data = json_data | {key: args[key]} if (args[key] or args[key] in (0, [], "")) else json_data
        r = self.get_api_users_list(url_params={"page": page})
        r.assert_status_code(expected_status_code)
        return r
