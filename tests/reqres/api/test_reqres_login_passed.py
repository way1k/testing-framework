import allure


@allure.title("Успешная авторизация")
@allure.label("platform", "Reqres")
def test_reqres_login_passed(api_reqres):

    with allure.step("Проверить успешную авторизацию"):
        api_reqres.actions.common.api_login_with(
            email="eve.holt@reqres.in",
            password="cityslicka",
        )


