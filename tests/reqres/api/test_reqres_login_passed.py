import allure


@allure.title("Successful authorization")
@allure.label("platform", "Reqres")
def test_reqres_login_passed(reqres_service):

    with allure.step("Verify successful authorization"):
        r = reqres_service.methods.method_api_login_with(email="eve.holt@reqres.in", password="cityslicka")
        r.validate(reqres_service.models.post_api_login.ok)


@allure.title("Not successful authorization")
@allure.label("platform", "Reqres")
def test_reqres_login_failed(reqres_service):

    with allure.step("Verify failed authorization"):
        r = reqres_service.methods.method_api_login_with(email="", password="111", expected_status_code=400)
        r.validate(reqres_service.models.post_api_login.bad_request)
