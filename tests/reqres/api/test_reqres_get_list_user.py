import allure


@allure.title("Successful request for user information")
@allure.label("platform", "Reqres")
def test_reqres_get_list_users_successful(reqres_service):

    with allure.step("Check to get a list of users on the second page"):
        r = reqres_service.methods.method_get_list_users(page=2)
        r.validate(reqres_service.models.get_api_users_list.ok)


@allure.title("Check email")
@allure.label("platform", "Reqres")
def test_reqres_get_list_users_check_email(reqres_service):

    with allure.step("Check to get a list of users on the second page"):
        r = reqres_service.methods.method_get_list_users(page=2)
        r.validate(reqres_service.models.get_api_users_list.ok)

    with allure.step("Check email exist"):
        reqres_service.helpers.get_api_users_list.check_email_by_user(
            response=r, user_number=2, expected_email="lindsay.ferguson@reqres.in"
        )
        reqres_service.helpers.get_api_users_list.check_email_by_user(
            response=r, user_number=3, expected_email="tobias.funke@reqres.in"
        )
