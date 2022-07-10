import allure


@allure.title("Specially falling test")
@allure.label("platform", "Bashorg")
def test_bashorg_failed():

    with allure.step("Open the main page"):
        assert 1 == 0
