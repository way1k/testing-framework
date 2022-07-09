from tools.asserts import Asserts
from tools.response_validate import ResponseValidate


class GetApiUsersList:
    @staticmethod
    def check_email_by_user(response: ResponseValidate, user_number: int, expected_email: str) -> None:
        actual_email = response.get_value(f"data[{user_number-1}].email")
        Asserts.equal(
            value=actual_email,
            expected_value=expected_email,
            msg=f"Asserting expected email: '{expected_email}' is equal actual email: '{actual_email}'",
            err_msg=f"Expected email: '{expected_email}' is not equal actual email: '{actual_email}'",
        )

    @staticmethod
    def check_some_param_2(response: ResponseValidate) -> None:
        pass
