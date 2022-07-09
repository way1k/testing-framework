import allure


@allure.title("Specially passing test")
@allure.label("platform", "Bashorg")
def test_bashorg_passed(platform):

    with allure.step("Open the home page"):
        assert 1 == 1
