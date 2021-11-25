import glob
import allure
import pytest
import logging
import os.path
import urllib3
from dotenv import load_dotenv
from inspect import currentframe
from tools.browser.browser_setup import Browser
from api_methods.procedure_api import BackAPI
from settings import CONFIG_DIR, LOCAL_FILES_DIR, PROJECT_DIR


pytest_plugins = [
    "plugins.reporter.plugin",
    "fixtures.platform_name_example.database"
]

logging.getLogger("requests").setLevel(logging.INFO)
logging.getLogger("urllib3").setLevel(logging.CRITICAL)
logging.getLogger("selenium").setLevel(logging.INFO)
logging.getLogger("faker").setLevel(logging.WARNING)
urllib3.disable_warnings()
logging.captureWarnings(True)


@pytest.fixture(scope="function")
def platform(request):
    bash_url = os.environ.get("BASHORG_URL")
    reqres_url = os.environ.get("REQRES_URL")
    module_name = str(currentframe().f_locals['request']).replace("<SubRequest \'platform\' for <Function ", "")[0:-2]
    test_name = __get_test_name(module_name)

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
                    attachment_type=allure.attachment_type.PNG
                )
    except AttributeError:
        pass

    browser.wd.quit()


@pytest.fixture(scope="function")
def api_reqres():
    reqres_url = os.environ.get("REQRES_URL")
    api = BackAPI(base_url=reqres_url)
    yield api
    api.client.close_session()


@pytest.fixture(scope="session")
def cleanup_tmp():
    directory = f"{LOCAL_FILES_DIR}/*"
    for clean_up in glob.glob(directory):
        if not clean_up.endswith('.gitkeep'):
            os.remove(clean_up)
    yield
    for clean_up in glob.glob(directory):
        if not clean_up.endswith('.gitkeep'):
            os.remove(clean_up)


@pytest.fixture(scope="session", autouse=True)
def load_env(request):
    environment = request.config.getoption("--env")
    dotenv_path = os.path.join(CONFIG_DIR, f".env.{environment}")
    load_dotenv(dotenv_path, override=True)


@pytest.hookimpl(hookwrapper=True, tryfirst=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    rep = outcome.get_result()
    setattr(item, "rep_" + rep.when, rep)
    return rep


@pytest.fixture(scope="session")
def storage(request):
    return request.config.getoption("--browser")


@pytest.fixture(scope="function")
def traceback_on_failure(request):
    yield
    if request.node.rep_setup.failed:
        traceback = request.node.rep_setup.longreprtext
        allure.attach(traceback, name='traceback', attachment_type=allure.attachment_type.TEXT)
    elif request.node.rep_setup.passed:
        if request.node.rep_call.failed:
            traceback = request.node.rep_call.longreprtext
            allure.attach(traceback, name='traceback', attachment_type=allure.attachment_type.TEXT)


def pytest_collection_modifyitems(items):
    for item in items:

        if "/api" in item.fspath.dirname:
            item.add_marker(pytest.mark.api)

        elif "/ui" in item.fspath.dirname:
            item.add_marker(pytest.mark.ui)

        for mark in item.iter_markers(name="allure_label"):

            if mark.kwargs == {'label_type': 'platform'}:
                components = mark.args
                for component in components:
                    item.add_marker(component.lower())


def __get_test_name(file_name):
    search_file = file_name + '.py'
    for root, dirs, files in os.walk(f"{PROJECT_DIR}/tests"):
        if search_file in files:
            with open(str(os.path.join(root, search_file)), "r", encoding='utf-8') as f:
                lines = f.readlines()
            chains = [line for line in lines if line.startswith("@allure.title(")]
            test_name = chains[0].replace('@allure.title("', '')[:-3]
            return test_name + ' | ' + '\n' + search_file


def pytest_addoption(parser):
    parser.addoption("--browser", action="store", default="local")
    parser.addoption('--browser_version', action="store", default="92.0")
    parser.addoption("--env", action="store", default="dev")
    parser.addoption("--log_level", action="store", default="INFO")
    parser.addoption("--report", action="store", default="yes")
