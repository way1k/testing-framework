import allure


@allure.title("Проверка наличия блоков меню")
@allure.label("platform", "Bashorg")
def test_bashorg_blocks_avaliable(platform):

    with allure.step("Открыть главную страницу"):
        platform.bash_org.main_page.open_main_page()

    with allure.step("Проверить наличие верхнего блока меню"):
        platform.bash_org.main_page.check_upper_block_menu()

    with allure.step("Проверить наличие нижнего блока меню"):
        platform.bash_org.main_page.check_down_block_menu()

