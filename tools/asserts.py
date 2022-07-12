import logging
from typing import Sized

import allure
from hamcrest import (
    assert_that,
    empty,
    greater_than,
    greater_than_or_equal_to,
    is_in,
    is_not,
    less_than_or_equal_to,
    not_,
)


class Asserts:
    """
    Common asserts
    """

    @staticmethod
    def equal_as_lists(list1: list, list2: list, msg: str | None = None) -> None:
        """Matches if list_1 equal to list_2"""
        if msg is None:
            msg = f"\nComparing two lists. \nlist1: '{list1}' \nlist2: '{list2}'"
        logging.info(msg)
        with allure.step(msg):
            if len(list1) != len(list2):
                raise AssertionError("Lists of different length")
            for index, elem in enumerate(list1):
                assert (
                    elem == list2[index]
                ), f"Found different elements on index {index}: \n{elem} \nvs \n{list2[index]}"

    @staticmethod
    def all_true(data: list, err_msg: str | None = None, msg: str | None = None) -> None:
        """Matches if all elements is true"""
        if msg is None:
            msg = f"Asserting that all values in {data} true"
        if err_msg is None:
            err_msg = f"Expected that all values in {data} are true"
        logging.info(msg)
        with allure.step(msg):
            assert all(data), err_msg

    @staticmethod
    def all_false(data: list, err_msg: str | None = None, msg: str | None = None) -> None:
        """Matches if all elements is false"""
        if msg is None:
            msg = f"Asserting that all values in {data} false"
        if err_msg is None:
            err_msg = f"Expected that all values in {data} are false"
        logging.info(msg)
        with allure.step(msg):
            assert not any(data), err_msg

    @staticmethod
    def contains(
        element: str | list | set,
        sub_element: str | list | set | int | float,
        sub_element_2: str | int | float | None = None,
        err_msg: str | None = None,
        msg: str | None = None,
    ) -> None:
        """Matches if element contains sub_element"""
        if err_msg is None:
            err_msg = (
                f'Expected element:\n"{element}" \ncontains \n"{sub_element}" \nor \n"{sub_element_2}"'
                if sub_element_2
                else f"Expected {element} contains {sub_element}"
            )
        if msg is None:
            msg = (
                f'Asserting element:\n"{element}" \ncontains: \n"{sub_element}" \nor \n"{sub_element_2}"'
                if sub_element_2
                else f"Asserting {element} contains {sub_element}"
            )

        logging.info(msg)
        with allure.step(msg):
            try:
                if isinstance(element, (list, set, tuple)) and isinstance(sub_element, (list, set, tuple)):
                    assert set(sub_element).issubset(element)
                elif isinstance(element, (list, set, tuple, str)) and isinstance(sub_element, (int, float, str)):
                    if sub_element_2:
                        assert sub_element in element or sub_element_2 in element
                    else:
                        assert sub_element in element
            except AssertionError:
                allure.attach(name="element", body=str(element), attachment_type=allure.attachment_type.TEXT)
                allure.attach(name="sub_element", body=str(sub_element), attachment_type=allure.attachment_type.TEXT)
                if sub_element_2:
                    allure.attach(
                        name="sub_element_2", body=str(sub_element_2), attachment_type=allure.attachment_type.TEXT
                    )
                raise AssertionError(err_msg)

    @staticmethod
    def not_contains(
        element: any, sub_element: str | list | set, err_msg: str | None = None, msg: str | None = None
    ) -> None:
        """Matches if element not contains sub_element"""
        if err_msg is None:
            err_msg = f"Expected '{element}' not contains '{sub_element}'"
        if msg is None:
            msg = f"Asserting '{element}' not contains '{sub_element}'"
        logging.info(msg)
        with allure.step(msg):
            assert_that(sub_element, not_(is_in(element)), err_msg)

    @staticmethod
    def not_equal(value, new_value, err_msg: str | None = None, msg: str | None = None) -> None:
        """Matches if value not equal to expected_value"""
        if err_msg is None:
            err_msg = f"Expected that {value} not equal to {new_value}"
        if msg is None:
            msg = f"Asserting {value} not equal to {new_value}"
        logging.info(msg)
        with allure.step(msg):
            assert value != new_value, err_msg

    @staticmethod
    def equal(value, expected_value, err_msg: str | None = None, msg: str | None = None) -> None:
        """Matches if value equal to expected_value"""
        if err_msg is None:
            err_msg = f"Expected that {value} equal to {expected_value}"
        if msg is None:
            msg = f"Asserting {value} equal to {expected_value}"
        logging.info(msg)
        with allure.step(msg):
            allure.attach(name="expected", body=str(expected_value))
            allure.attach(name="value", body=str(value))
            assert value == expected_value, err_msg

    @staticmethod
    def true(value, err_msg: str | None = None, msg: str | None = None) -> None:
        """Matches if value is True"""
        if err_msg is None:
            err_msg = f"Expected that {value} is True"
        if msg is None:
            msg = f"Asserting {value} is True"
        logging.info(msg)
        with allure.step(msg):
            assert value is True, err_msg

    @staticmethod
    def false(value, err_msg: str | None = None, msg: str | None = None) -> None:
        """Matches if value is False"""
        if err_msg is None:
            err_msg = f"Expected that {value} is False"
        if msg is None:
            msg = f"Asserting {value} is False"
        logging.info(msg)
        with allure.step(msg):
            assert value is False, err_msg

    @staticmethod
    def truthy(value, err_msg: str | None = None, msg: str | None = None) -> None:
        """Matches if value is truthy"""
        if err_msg is None:
            err_msg = f"Expected that {value} is truthy"
        if msg is None:
            msg = f"Asserting {value} is truthy"
        logging.info(msg)
        with allure.step(msg):
            assert value, err_msg

    @staticmethod
    def falthy(value, err_msg: str | None = None, msg: str | None = None) -> None:
        """Matches if value is falthy"""
        if err_msg is None:
            err_msg = f"Expected that {value} is falthy"
        if msg is None:
            msg = f"Asserting {value} is falthy"
        logging.info(msg)
        with allure.step(msg):
            assert not value, err_msg

    @staticmethod
    def more_or_equal(
        value_1: int | float, value_2: int | float, err_msg: str | None = None, msg: str | None = None
    ) -> None:
        """Matches if value_1 is more than or equal to a given value_2."""
        if err_msg is None:
            err_msg = f"Expected that {value_1} is more or equal then {value_2}"
        if msg is None:
            msg = f"Asserting that {value_1} is more or equal then {value_2}"
        logging.info(msg)
        with allure.step(msg):
            assert_that(value_1, greater_than_or_equal_to(value_2), err_msg)

    @staticmethod
    def less_or_equal(
        value_1: int | float, value_2: int | float, err_msg: str | None = None, msg: str | None = None
    ) -> None:
        """Matches if value_1 is less than or equal to a given value_2."""
        if err_msg is None:
            err_msg = f"Expected that {value_1} is less or equal then {value_2}"
        if msg is None:
            msg = f"Asserting that {value_1} is less or equal then {value_2}"
        logging.info(msg)
        with allure.step(msg):
            assert_that(value_1, less_than_or_equal_to(value_2), err_msg)

    @staticmethod
    def more(value_1: int | float, value_2: int | float, err_msg: str | None = None, msg: str | None = None) -> None:
        """Matches if value_1 is more than a given value_2."""
        if err_msg is None:
            err_msg = f"Expected that {value_1} is more then {value_2}"
        if msg is None:
            msg = f"Asserting that {value_1} is more then {value_2}"
        logging.info(msg)
        with allure.step(msg):
            assert_that(value_1, greater_than(value_2), err_msg)

    @staticmethod
    def not_empty(collection: Sized, err_msg: str | None = None, msg: str | None = None) -> None:
        """Matches if collection is not empty"""
        if err_msg is None:
            err_msg = f"Expected that {collection} is not empty"
        if msg is None:
            msg = f"Asserting that {collection} is not empty"
        logging.info(msg)
        with allure.step(msg):
            assert_that(collection, is_not(empty()), err_msg)
