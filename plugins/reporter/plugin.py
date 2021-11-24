import getpass
import os
import time

import pytest
from plugins.reporter import api, utils
from plugins.reporter.utils import get_active_branch_name, get_platform
from settings import ALLURE_REPORT, LOCAL_FILES_DIR


ALLURE_RESULTS_ZIP = LOCAL_FILES_DIR + "/allure_results.zip"
ALLURE_ENVIRONMENT_PROPERTIES_FILE = "environment.properties"
TEST_RESULTS = []


def pytest_configure(config):
    if config.getoption('report') == 'yes':
        config.option.allure_report_dir = ALLURE_REPORT["results_dir"]


def pytest_sessionfinish(session):

    if session.config.option.allure_report_dir:
        allure_dir = session.config.option.allure_report_dir
    else:
        return


    # assert os.path.isdir(allure_dir), f"Папки {allure_dir} не существует"

    try:
        server_url = ALLURE_REPORT["url"]
        client = api.AllureServer(server_url)
        path = os.environ.get("GITLAB_USER_LOGIN") or getpass.getuser()

        # utils.print_(f"Генерируется отчет для \"{path}\"...")

        branch_name = get_active_branch_name()
        path += f"/{branch_name}"

        platform_name = get_platform(session.config)
        path = f"{platform_name}/" + path

        rep_num = client.get_build_num(path)
        path += f"/{rep_num}"

        time.sleep(10)
        trigger = client.is_reports(path)

        if trigger:
            return
        else:

            utils.compress_to_zip(
                folder=allure_dir,
                zip_name=ALLURE_RESULTS_ZIP
            )

            rep_link = client.generate_report(
                client.send_results(ALLURE_RESULTS_ZIP),
                path
            )

        # stand = _get_stand(request=session)

        # if "prod" in path:
        #     for file in glob.glob(f"{allure_dir}/*-result.json"):
        #         with open(file, "r") as f:
        #             TEST_RESULTS.append(_parse_data_from_json(f, stand))

            if rep_link:
                os.environ["ALLURE_REPORT_URL"] = rep_link
                utils.print_("-" * 80)
                utils.print_(f"Сгенерирован отчет для \"{os.environ.get('GITLAB_USER_LOGIN') or getpass.getuser()}\"")
                utils.print_(f"Ссылка на отчет: {rep_link}")
            else:
                utils.print_("Не удалось сгенерировать отчет...")
            utils.print_("-" * 80)
    finally:
        utils.cleanup(ALLURE_RESULTS_ZIP, allure_dir)


@pytest.fixture(scope="session", autouse=True)
def add_environment_property(request):
    properties = {}
    stage = request.config.getoption("--env")
    properties['Stage'] = stage

    yield

    allure_dir = request.session.config.option.allure_report_dir
    if not allure_dir or not os.path.isdir(allure_dir) or len(properties) == 0:
        return

    allure_env_path = os.path.join(allure_dir, ALLURE_ENVIRONMENT_PROPERTIES_FILE)
    with open(allure_env_path, "w") as f:
        data = "\n".join([f"{variable}={value}" for variable, value in properties.items()])
        f.write(data)






# def _parse_data_from_json(file, stand):
#     result = {}
#     raw = json.load(file)
#     result["name"] = raw.get("name")
#     result["status"] = raw.get("status")
#     result["mark"] = _get_tflo_mark(raw.get("labels", []))
#     result["duration"] = round(((raw.get("stop", 0) - raw.get("start", 0)) / 1000), 2)
#     result["date"] = str(datetime.now().strftime("%Y-%m-%d %X"))
#     result["stand"] = stand
#     result["log"] = raw.get("statusDetails", {}).get("message")
#
#     return result
