import json
import logging
import uuid
from typing import Any, Callable

import allure
from requests import Request

from tools.response_validate import ResponseValidate


class Endpoint:
    """
    Abstract class for clients of services

    For implementation HTTP methods use class Endpoint.
    Methods naming rules:

    <method><api_version/any_prefix>_<operationId>, where

    operationId - method name
    api_version/any_prefix - version or some prefix

    For example:
    POST /api/register - post_api_register()
    """

    url = str()
    method = str()

    def __init__(
        self, method: str, url: str, base_url: str | None = "REQRES_URL", version: str = "", prefix: str = ""
    ) -> None:

        self.method = method
        self.base_url = base_url
        self.version = version if not prefix else prefix
        self.url = url

    def __set_name__(self, owner: type, name: str) -> None:
        self.name = name

    def __get__(
        self, instance, owner
    ) -> Callable[[dict | None, dict | None, str | None, dict[str, Any]], ResponseValidate]:
        def perform_request(
            source_url_params: dict | None = None,
            url_params: dict | None = None,
            token: str | None = None,
            **req_kwargs: dict[str, Any],
        ) -> ResponseValidate:

            request = Request(**req_kwargs)
            request.method = self.method

            cfg_url = getattr(instance.cfg, self.base_url)

            source_url_params = dict() if not source_url_params else source_url_params
            path_url = (
                f"{self.version}{self.url.format(**source_url_params)}"
                if source_url_params
                else f"{self.version}{self.url}"
            )

            url_params = dict() if not url_params else url_params
            parsed_url = "&".join([f"{key}={value}" for key, value in url_params.items()])

            path_url = path_url + "?" + parsed_url if parsed_url else path_url
            url = cfg_url + path_url

            request.url = url

            request.headers.update({"X-Request-Token": str(uuid.uuid4())})
            if token:
                instance.session["token"] = str(token)

            prepared_request = request.prepare()
            req_log_rec = dict()
            req_log_rec["method"] = prepared_request.method
            req_log_rec["url"] = prepared_request.url
            req_log_rec["headers"] = {k: v for k, v in prepared_request.headers.items()}

            if prepared_request.body is not None:
                try:
                    body = json.loads(prepared_request.body)
                except json.JSONDecodeError:
                    body = prepared_request.body

                req_log_rec["body"] = body

            service_name = owner.__doc__.split(" service")[0]
            logging.info(f"Request to {service_name} --> {self.method.upper()} {path_url}")

            with allure.step(f"Request to {service_name} --> {self.method.upper()} {path_url}"):
                response = instance.session.send(prepared_request)
            logging.debug("HTTP request: %s", json.dumps(req_log_rec))

            if response is not None:
                resp_log_rec = dict()
                resp_log_rec["url"] = response.url
                resp_log_rec["status_code"] = response.status_code

                if response.text:
                    try:
                        body = json.loads(response.text)
                    except json.JSONDecodeError:
                        body = response.text

                    resp_log_rec["body"] = body
                    resp_log_rec["headers"] = dict(response.headers)

                logging.debug("HTTP response: %s", json.dumps(resp_log_rec))
            else:
                logging.debug("HTTP response: %s", response)

            return ResponseValidate(response)

        return perform_request
