import getpass
import os
from logging import error as elog

import pytest
from _pytest.config import Config
from _pytest.fixtures import SubRequest
from _pytest.main import Session
from xdist import get_xdist_worker_id

from plugins.reporter_allure.api_allure_docker_ui import AllureDockerService
from plugins.reporter_allure.api_allure_server import AllureServer
from plugins.reporter_allure.utils import cleanup, compress_to_zip, get_active_branch_name, get_platform, print_
from settings import ALLURE_DOCKER_UI, ALLURE_SERVER, LOCAL_FILES_DIR

ALLURE_RESULTS_ZIP = LOCAL_FILES_DIR + "/allure_results.zip"
ALLURE_ENVIRONMENT_PROPERTIES_FILE = "environment.properties"
TEST_RESULTS = []


def pytest_configure(config: Config) -> None:
    if config.getoption("report") == "enable":
        config.option.allure_report_dir = ALLURE_SERVER["results_dir"]


@pytest.fixture(scope="session", autouse=True)
def add_environment_property(request: SubRequest) -> None:
    properties = dict()
    properties["STAGE"] = request.config.getoption("--env")
    properties["BROWSER"] = request.config.getoption("--browser")
    properties["BROWSER_VERSION"] = request.config.getoption("--browser_version")
    properties["LOG_LEVEL"] = request.config.getoption("--log_level")
    properties["MARKERS"] = request.config.getoption("-m")

    yield

    allure_dir = request.session.config.option.allure_report_dir
    if not allure_dir or not os.path.isdir(allure_dir) or len(properties) == 0:
        return

    allure_env_path = os.path.join(allure_dir, ALLURE_ENVIRONMENT_PROPERTIES_FILE)
    with open(allure_env_path, "w") as f:
        data = "\n".join([f"{variable}={str(value).upper()}" for variable, value in properties.items()])
        f.write(data)


def pytest_sessionfinish(session: Session) -> None:
    if session.config.option.allure_report_dir and get_xdist_worker_id(session) == "master":
        allure_dir = session.config.option.allure_report_dir
    else:
        return

    if len(os.listdir(allure_dir)) == 0:
        return elog(f"Dir with allure results {allure_dir} is empty. Reports does not generate.")

    try:
        client_docker = AllureDockerService(
            ALLURE_DOCKER_UI["url"], ALLURE_DOCKER_UI["project_id"], ALLURE_DOCKER_UI["results_dir"]
        )
        client_docker.clean_results()
        client_docker.send_results()
        rep_link_allure_docker = client_docker.generate_report()

        compress_to_zip(folder=allure_dir, zip_name=ALLURE_RESULTS_ZIP)

        client = AllureServer(ALLURE_SERVER["url"])

        path = os.environ.get("GITLAB_USER_LOGIN") or getpass.getuser()

        print_("-" * 80)
        print_(f'A report is generated for "{path}"...')

        branch_name = get_active_branch_name()
        path += f"/{branch_name}"

        platform_name = get_platform(session.config)
        path = f"{platform_name}/" + path

        rep_num = client.get_build_num(path)
        path += f"/{rep_num}"

        rep_link_server = client.generate_report(client.send_results(ALLURE_RESULTS_ZIP), path)

        if rep_link_server and rep_link_allure_docker:
            os.environ["ALLURE_SERVER_REPORT_URL"] = rep_link_server
            print_("ALLURE SERVER REPORT URL:")
            print_(rep_link_server)
            os.environ["ALLURE_DOCKER_REPORT_URL"] = rep_link_allure_docker
            print_("ALLURE DOCKER REPORT URL:")
            print_(rep_link_allure_docker)
        else:
            print_("Failed to generate report...")
        print_("-" * 80)
    finally:
        cleanup(ALLURE_RESULTS_ZIP, allure_dir)
