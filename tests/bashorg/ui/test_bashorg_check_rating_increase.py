import allure


@allure.title("Checking the rating increase on the random citation page")
@allure.label("platform", "Bashorg")
def test_bashorg_check_rating_increase(platform):

    with allure.step("Open the main page"):
        platform.bash_org.main_page.open_main_page()

    with allure.step("Go to the 'random' tab"):
        platform.bash_org.main_page.select_type_quotes_in_upper_block(quotes_type="случайные")

    with allure.step("Check the quote's rating increase"):
        actual_rating = platform.bash_org.random_page.get_actual_quote_rating(quote_number=1)
        platform.bash_org.random_page.increase_rating(quote_number=1)
        platform.bash_org.random_page.assert_increase_rating(rating_before=actual_rating, quote_number=1)
