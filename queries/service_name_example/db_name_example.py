from hamcrest import assert_that, is_not, empty

"""
Модуль запросов к базе db_name_example сервиса service_name_example
"""


def get_item(db_name_fixture, item):
    query = f"""SELECT y.id 
                FROM x 
                WHERE z = {item};"""
    query_result = db_name_fixture.fetchone_result(query, wait_retries=5)
    assert_that(query_result, is_not(empty()))
    return query_result['id']
