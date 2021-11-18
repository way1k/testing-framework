import allure


@allure.title("Успешный запрос на получение информации о пользователях")
@allure.label("platform", "Reqres")
def test_reqres_get_list_users(api_reqres):

    with allure.step("Проверить получение списка пользователей на второй странице"):
        users_data = api_reqres.actions.users.get_list_users_by_page_number(
            page_number=2
        )

    with allure.step("Проверить наличие email пользователя в списке"):
        api_reqres.actions.users.check_email_in_list_of_users(
            users_data=users_data,
            expected_email="tobias.funke@reqres.in"
        )


