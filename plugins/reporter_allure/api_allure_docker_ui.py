import base64
import json
import os
from logging import error as elog

from requests import Session

from settings import ALLURE_FILES_DIR


class AllureDockerService:
    def __init__(self, url: str, project_id: str, results_directory: str = ALLURE_FILES_DIR) -> None:
        self.url = url
        self.project_id = project_id
        self.results_directory = results_directory
        self.ssl_verification = True
        self._session = Session()

    def send_results(self) -> None:
        files = os.listdir(self.results_directory)

        results = []
        for file in files:
            result = {}

            file_path = self.results_directory + "/" + file

            if os.path.isfile(file_path):
                try:
                    with open(file_path, "rb") as f:
                        content = f.read()
                        if content.strip():
                            b64_content = base64.b64encode(content)
                            result["file_name"] = file
                            result["content_base64"] = b64_content.decode("UTF-8")
                            results.append(result)
                        else:
                            print("Empty File skipped: " + file_path)
                finally:
                    f.close()
            else:
                print("Directory skipped: " + file_path)

        headers = {"Content-type": "application/json"}
        request_body = {"results": results}
        json_request_body = json.dumps(request_body)
        r = self._session.post(
            self.url + "/allure-docker-service/send-results?project_id=" + self.project_id,
            headers=headers,
            data=json_request_body,
            verify=self.ssl_verification,
        )
        if not r.ok:
            elog(f"The results have not been sent to the allure-docker-ui-server. Invalid response: {r.text}")
        return

    def generate_report(
        self, exec_name: str = "python executor", exec_from: str = "local", exec_type: str = "gitlab"
    ) -> None | str:
        headers = {"Content-type": "application/json"}
        r = self._session.get(
            self.url
            + "/allure-docker-service/generate-report?project_id="
            + self.project_id
            + "&execution_name="
            + exec_name
            + "&execution_from="
            + exec_from
            + "&execution_type="
            + exec_type,
            headers=headers,
            verify=self.ssl_verification,
        )
        if not r.ok:
            elog(f"Failed to generate report for allure-docker-service-ui. Invalid response: {r.text}")
            return
        return json.loads(r.content)["data"]["report_url"]

    def clean_results(self) -> None | str:
        headers = {"Content-type": "application/json"}
        r = self._session.get(
            self.url + "/allure-docker-service/clean-results?project_id=" + self.project_id,
            headers=headers,
            verify=self.ssl_verification,
        )
        if not r.ok:
            elog(f"Failed to clean results for allure-docker-service-ui. Invalid response: {r.text}")
        return
