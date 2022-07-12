from tools.asserts import Asserts


class DBNameQueries:
    """
    Queries class for requests to db_name_example
    """


def get_item(db_name_fixture, item: str) -> int:
    query = f"""SELECT y.id  FROM x WHERE z = {item};"""
    query_result = db_name_fixture.fetchone_result(query, wait_retries=5)
    Asserts.not_empty(query_result)
    return query_result["id"]
