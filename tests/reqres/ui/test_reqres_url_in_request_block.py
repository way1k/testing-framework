import allure


@allure.title("Successful request for user information")
@allure.label("platform", "Reqres")
def test_reqres_url_in_request_block(platform):

    with allure.step("Open the home page"):
        platform.reqres.main_page.open_main_page()

    with allure.step("Check the url for the 'SINGLE_USER' button"):
        platform.reqres.main_page.click_button_single_user()
        platform.reqres.main_page.check_url_in_request_block(expected_url="/api/users/2")

    with allure.step("Check the url for the 'LIST_USERS' button"):
        platform.reqres.main_page.click_button_list_users()
        platform.reqres.main_page.check_url_in_request_block(expected_url="/api/users?page=2")

    with allure.step("Check the url for the 'SINGLE_USER_NOT_FOUND' button"):
        platform.reqres.main_page.click_button_user_not_found()
        platform.reqres.main_page.check_url_in_request_block(expected_url="/api/users/23")
