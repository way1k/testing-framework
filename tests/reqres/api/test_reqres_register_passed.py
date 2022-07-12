import allure


@allure.title("Successful registration")
@allure.label("platform", "Reqres")
def test_reqres_register_passed(reqres_service):

    with allure.step("Verify successful user registration"):
        r = reqres_service.methods.method_api_register(email="eve.holt@reqres.in", password="pistol")
        r.validate(reqres_service.models.post_api_register.ok)
