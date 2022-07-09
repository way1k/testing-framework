import json
import logging
import re
from typing import Any

from pydantic import ValidationError
from requests import Response

from tools.asserts import Asserts


class ResponseValidate:
    """
    Class-wrapper for work with responses (validating by pydantic schema , asserting, etc)
    """

    def __init__(self, response: Response) -> None:
        self.source_response = response
        self.request_json = json.loads(response.request.body) if response.request.body else None
        self.response_json = response.json()
        self.response_status_code = response.status_code
        self.parsed_object = None

    def validate(self, schema):
        logging.debug(f"Validating response data by pydantic schema '{schema.__name__}'")
        logging.debug(f"Json schema {schema.schema_json()}")
        try:
            if isinstance(self.response_json, list):
                self.parsed_object = list()
                for item in self.response_json:
                    parsed_object = schema.parse_obj(item)
                    self.parsed_object.append(parsed_object)
            else:
                self.parsed_object = schema.parse_obj(self.response_json)
        except ValidationError as e:
            raise ValueError(e.json())

    def assert_status_code(self, status_code: list | int) -> None:
        logging.debug(f"Asserting response status code for HTTP request to '{self.source_response.url}'")
        if isinstance(status_code, list):
            Asserts.contains(
                element=status_code,
                sub_element=self.response_status_code,
                err_msg=f"Expected status codes '{status_code}' is not equal actual '{self.response_status_code}'",
            )
        else:
            Asserts.equal(
                value=self.response_status_code,
                expected_value=status_code,
                err_msg=f"Expected status code '{status_code}' is not equal actual '{self.response_status_code}'",
            )

    def get_parsed_object(self):
        return self.parsed_object

    def get_raw_object(self):
        return self.response_json

    def get_value(self, value_path: str):
        parsed_obj = self.get_parsed_object()
        return self.multi_getattr(parsed_obj, value_path)

    def assert_value_in_response(self, value_path: str, expected_value: Any) -> None:
        value = self.get_value(value_path)
        Asserts.equal(value=value, expected_value=expected_value)

    def assert_value_in_response_contains(self, value_path: str, expected_value: Any) -> None:
        value = self.get_value(value_path)
        Asserts.contains(element=value, sub_element=expected_value)

    @staticmethod
    def multi_getattr(obj, value_path: str, default=None):
        attributes = value_path.split(".")
        for i in attributes:
            try:
                obj = getattr(obj, i.split("[")[0])
                result = re.findall(r"\[([\s\S]+?)\]", i)
                if result:
                    for index in result:
                        obj = obj[int(index)]
            except AttributeError:
                if default:
                    return default
                else:
                    raise
        return obj

    def __str__(self):
        return (
            f"\nStatus code: {self.response_status_code}"
            f"\nRequested url: {self.source_response.url}"
            f"\nResponse body: {self.response_json}"
        )


response_validate = ResponseValidate
