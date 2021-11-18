import allure


@allure.title("Успешный запрос на получение информации о пользователе")
@allure.label("platform", "Reqres")
def test_reqres_get_user(api_reqres):

    with allure.step("Проверить получение информации по пользователю с заданным id"):
        api_reqres.actions.users.get_user_by_id(
            user_id=2
        )


