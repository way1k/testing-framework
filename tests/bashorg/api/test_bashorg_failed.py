import time
import allure


@allure.title("Специально падающий тест")
@allure.label("platform", "Bashorg")
def test_bashorg_failed(platform):

    with allure.step("Открыть главную страницу"):
        time.sleep(60)
        assert 1 == 0

