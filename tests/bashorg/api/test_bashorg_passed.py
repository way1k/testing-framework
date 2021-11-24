import time
import allure


@allure.title("Специально успешно проходящий тест")
@allure.label("platform", "Bashorg")
def test_bashorg_passed(platform):

    with allure.step("Открыть главную страницу"):
        time.sleep(60)
        assert 1 == 1

