import allure


@allure.title("Проверка открытия главной страницы bashorg")
@allure.label("platform", "Bashorg")
def test_bashorg_open(platform):

    with allure.step("Открыть главную страницу"):
        platform.bash_org.main_page.open_main_page()

