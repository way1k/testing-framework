import allure


@allure.title("Successful request for user information")
@allure.label("platform", "Reqres")
def test_reqres_get_user_successful(reqres_service):

    with allure.step("Check receive information about user by user_id"):
        r = reqres_service.methods.method_get_user_by_id(user_id=2)
        r.validate(reqres_service.models.get_api_users.ok)


@allure.title("Not successful request for user information")
@allure.label("platform", "Reqres")
def test_reqres_get_user_not_successful(reqres_service):

    with allure.step("Check receive not found response"):
        r = reqres_service.methods.method_get_user_by_id(user_id=1000, expected_status_code=404)
        r.validate(reqres_service.models.get_api_users.not_found)
