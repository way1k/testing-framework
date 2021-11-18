import allure


@allure.title("Проверка увеличения рейтинга на странице рандомных цитат")
@allure.label("platform", "Bashorg")
def test_check_rating_increase(platform):

    with allure.step("Открыть главную страницу"):
        platform.bash_org.main_page.open_main_page()

    with allure.step("Перейти на вкладку 'случайные'"):
        platform.bash_org.main_page.select_type_quotes_in_upper_block(
            quotes_type='случайные'
        )

    with allure.step("Проверить увеличение рейтинга у цитаты"):
        actual_rating = platform.bash_org.random_page.get_actual_quote_rating(quote_number=1)
        platform.bash_org.random_page.increase_rating(quote_number=1)
        platform.bash_org.random_page.assert_increase_rating(
            rating_before=actual_rating,
            quote_number=1
        )

