import glob
import logging
import os.path
from inspect import currentframe

import allure
import pytest
import urllib3
from _pytest.config import Config
from _pytest.config.argparsing import Parser
from _pytest.fixtures import SubRequest
from _pytest.python import Function
from _pytest.reports import TestReport
from _pytest.runner import CallInfo
from dotenv import load_dotenv

from settings import CONFIG_DIR, LOCAL_FILES_DIR, PROJECT_DIR
from tools.browser.browser_setup import Browser
from tools.cfg_singleton import config_obj
from tools.session_singleton import http_session

pytest_plugins = ["fixtures.services", "plugins.reporter_allure.plugin", "fixtures.service_name_example.database"]

logging.getLogger("requests").setLevel(logging.INFO)
logging.getLogger("urllib3").setLevel(logging.CRITICAL)
logging.getLogger("selenium").setLevel(logging.INFO)
logging.getLogger("faker").setLevel(logging.WARNING)
urllib3.disable_warnings()
logging.captureWarnings(True)


@pytest.fixture(scope="function")
def platform(request: SubRequest) -> Browser:
    bash_url = os.environ.get("BASHORG_URL")
    reqres_url = os.environ.get("REQRES_URL")
    test_name = __get_test_name(request)

    browser = Browser(
        browser=request.config.getoption("--browser"),
        browser_version=request.config.getoption("--browser_version"),
        test_name=test_name,
        bash_url=bash_url,
        reqres_url=reqres_url,
    )

    yield browser

    try:
        if request.node.rep_setup.failed:
            logging.warning("Не удалось подготовить тестовую среду")
        elif request.node.rep_setup.passed:
            if request.node.rep_call.failed:
                allure.attach(
                    body=browser.wd.get_screenshot_as_png(),
                    name=request.function.__name__,
                    attachment_type=allure.attachment_type.PNG,
                )
    except AttributeError:
        pass

    browser.wd.quit()


@pytest.fixture(scope="session")
def cleanup_tmp() -> None:
    directory = f"{LOCAL_FILES_DIR}/*"
    for clean_up in glob.glob(directory):
        if not clean_up.endswith(".gitkeep"):
            os.remove(clean_up)
    yield
    for clean_up in glob.glob(directory):
        if not clean_up.endswith(".gitkeep"):
            os.remove(clean_up)


def pytest_configure(config: Config) -> None:
    environment = config.getoption("--env")
    dotenv_path = os.path.join(CONFIG_DIR, f".env.{environment}")
    load_dotenv(dotenv_path, override=True)

    for key in os.environ:
        if not hasattr(config_obj, key) or getattr(config_obj, key) != os.environ.get(key):
            setattr(config_obj, key, os.environ.get(key))


@pytest.fixture(scope="function", autouse=True)
def close_session() -> None:
    yield
    http_session.close_session()


@pytest.hookimpl(hookwrapper=True, tryfirst=True)
def pytest_runtest_makereport(item: Function, call: CallInfo) -> TestReport:
    outcome = yield
    rep = outcome.get_result()
    setattr(item, "rep_" + rep.when, rep)
    return rep


@pytest.fixture(scope="session")
def storage(request: SubRequest) -> str:
    return request.config.getoption("--browser")


@pytest.fixture(scope="function")
def traceback_on_failure(request: SubRequest):
    yield
    if request.node.rep_setup.failed:
        traceback = request.node.rep_setup.longreprtext
        allure.attach(traceback, name="traceback", attachment_type=allure.attachment_type.TEXT)
    elif request.node.rep_setup.passed:
        if request.node.rep_call.failed:
            traceback = request.node.rep_call.longreprtext
            allure.attach(traceback, name="traceback", attachment_type=allure.attachment_type.TEXT)


def pytest_collection_modifyitems(items: list[Function]) -> None:
    for item in items:

        if "/api" in item.fspath.dirname:
            item.add_marker(pytest.mark.api)

        elif "/ui" in item.fspath.dirname:
            item.add_marker(pytest.mark.ui)

        for mark in item.iter_markers(name="allure_label"):

            if mark.kwargs == {"label_type": "platform"}:
                components = mark.args
                for component in components:
                    item.add_marker(component.lower())


def __get_test_name(request: SubRequest) -> str:
    test_func_name = request.node.config.args[0].split("::")[-1]
    search_file = str(request.fspath).split("/")[-1]
    for root, dirs, files in os.walk(f"{PROJECT_DIR}/tests"):
        if search_file in files:
            with open(str(os.path.join(root, search_file)), "r", encoding="utf-8") as f:
                lines = list(reversed(f.readlines()))
            for index, line in enumerate(lines):
                if f"def {test_func_name}" in line:
                    lines = lines[index:]
                    break
            for line in lines:
                if line.startswith("@allure.title("):
                    test_name = line.replace('@allure.title("', "")[:-3]
            return test_name + " | " + "\n" + search_file


def pytest_addoption(parser: Parser) -> None:
    parser.addoption("--browser", action="store", default="local")
    parser.addoption("--browser_version", action="store", default="101.0")
    parser.addoption("--env", action="store", default="dev")
    parser.addoption("--log_level", action="store", default="DEBUG")
    parser.addoption("--report", action="store", default="disable")
