import allure


@allure.title("Успешная регистрация")
@allure.label("platform", "Reqres")
def test_reqres_register_passed(api_reqres):

    with allure.step("Проверить успешную регистрацию пользователя"):
        api_reqres.actions.common.api_register(
            email="eve.holt@reqres.in",
            password="pistol"
        )


