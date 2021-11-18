import allure


@allure.title("Успешная запрос на получение информации о пользователях")
@allure.label("platform", "Reqres")
def test_reqres_url_in_request_block(platform):

    with allure.step("Открыть главную страницу"):
        platform.reqres.main_page.open_main_page()

    with allure.step("Проверить url для кнопки 'SINGLE_USER'"):
        platform.reqres.main_page.click_button_single_user()
        platform.reqres.main_page.check_url_in_request_block(
            expected_url='/api/users/2'
        )

    with allure.step("Проверить url для кнопки 'LIST_USERS'"):
        platform.reqres.main_page.click_button_list_users()
        platform.reqres.main_page.check_url_in_request_block(
            expected_url='/api/users?page=2'
        )

    with allure.step("Проверить url для кнопки 'SINGLE_USER_NOT_FOUND'"):
        platform.reqres.main_page.click_button_user_not_found()
        platform.reqres.main_page.check_url_in_request_block(
            expected_url='/api/users/23'
        )



