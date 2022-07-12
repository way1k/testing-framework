import allure


@allure.title("Checking the presence of menu blocks")
@allure.label("platform", "Bashorg")
def test_bashorg_blocks_avaliable(platform):

    with allure.step("Open the main page"):
        platform.bash_org.main_page.open_main_page()

    with allure.step("Check the availability of the top menu bar"):
        platform.bash_org.main_page.check_upper_block_menu()

    with allure.step("Check the availability of the bottom menu bar"):
        platform.bash_org.main_page.check_down_block_menu()
