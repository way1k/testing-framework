import allure


@allure.title("Checking the opening of the bashorg home page")
@allure.label("platform", "Bashorg")
def test_bashorg_open(platform):

    with allure.step("Open the home page"):
        platform.bash_org.main_page.open_main_page()
