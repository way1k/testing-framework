import subprocess
from fixtures.app import *
from fixtures.common import *
from settings import PROJECT_DIR


def pytest_addoption(parser):

    parser.addoption(
        "--config",
        action="store",
        help="Test stand number",
        default="config_test_instagram"
    )

    parser.addoption(
        "--browser",
        action="store",
        help="Select browser",
        default="chrome",
    )

    parser.addoption(
        "--allure",
        action="store",
        help="Allure generate results",
        default="True",
    )


@pytest.fixture(scope="session", autouse=True)
def generate_report(pytestconfig):
    if pytestconfig.getoption('allure') == "True":
        yield
        subprocess.Popen("allure serve ALLURE_RESULTS", shell=True, cwd=PROJECT_DIR)
    elif pytestconfig.getoption('allure') == "False":
        yield print("Run tests without logs")
