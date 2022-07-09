import getpass
import os

import pytest
from _pytest.config import Config
from _pytest.fixtures import SubRequest
from _pytest.main import Session
from xdist import get_xdist_worker_id

from plugins.reporter import api, utils
from plugins.reporter.utils import get_active_branch_name, get_platform
from settings import ALLURE_REPORT, LOCAL_FILES_DIR

ALLURE_RESULTS_ZIP = LOCAL_FILES_DIR + "/allure_results.zip"
ALLURE_ENVIRONMENT_PROPERTIES_FILE = "environment.properties"
TEST_RESULTS = []


def pytest_configure(config: Config) -> None:
    if config.getoption("report") == "yes":
        config.option.allure_report_dir = ALLURE_REPORT["results_dir"]


@pytest.fixture(scope="session", autouse=True)
def add_environment_property(request: SubRequest) -> None:
    properties = {}
    stage = request.config.getoption("--env")
    properties["Stage"] = stage

    yield

    allure_dir = request.session.config.option.allure_report_dir
    if not allure_dir or not os.path.isdir(allure_dir) or len(properties) == 0:
        return

    allure_env_path = os.path.join(allure_dir, ALLURE_ENVIRONMENT_PROPERTIES_FILE)
    with open(allure_env_path, "w") as f:
        data = "\n".join([f"{variable}={value}" for variable, value in properties.items()])
        f.write(data)


def pytest_sessionfinish(session: Session) -> None:
    worker = get_xdist_worker_id(session)
    if session.config.option.allure_report_dir and worker == "master":
        allure_dir = session.config.option.allure_report_dir
    else:
        return

    assert os.path.isdir(allure_dir), f"Dir {allure_dir} is not exist"

    try:
        utils.compress_to_zip(folder=allure_dir, zip_name=ALLURE_RESULTS_ZIP)

        server_url = ALLURE_REPORT["url"]
        client = api.AllureServer(server_url)

        path = os.environ.get("GITLAB_USER_LOGIN") or getpass.getuser()

        utils.print_("-" * 80)
        utils.print_(f'A report is generated for "{path}"...')

        branch_name = get_active_branch_name()
        path += f"/{branch_name}"

        platform_name = get_platform(session.config)
        path = f"{platform_name}/" + path

        rep_num = client.get_build_num(path)
        path += f"/{rep_num}"

        rep_link = client.generate_report(client.send_results(ALLURE_RESULTS_ZIP), path)

        if rep_link:
            os.environ["ALLURE_REPORT_URL"] = rep_link
            utils.print_(f"Link to report: {rep_link}")

        else:
            utils.print_("Failed to generate report...")
        utils.print_("-" * 80)
    finally:
        utils.cleanup(ALLURE_RESULTS_ZIP, allure_dir)
