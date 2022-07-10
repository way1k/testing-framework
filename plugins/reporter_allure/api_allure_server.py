import os
from logging import error as elog

from requests import Session


class AllureServer:
    def __init__(self, url: str) -> None:
        self.url = url
        self._session = Session()

    def send_results(self, file_path: str) -> None | str:
        if not os.path.isfile(file_path):
            elog(f"ZIP-file was not found in the specified path: '{file_path}'")

        with open(file_path, "rb") as f:
            r = self._session.post(f"{self.url}/api/result", files={"allureResults": f})
        if not r.ok:
            elog(f"The results have not been sent to the server. Invalid response: {r.text}")
            return
        return r.json()["uuid"]

    def get_build_num(self, path: str) -> None | int:
        r = self._session.get(
            f"{self.url}/api/report?path={path}",
        )

        if not r.ok:
            elog(f"Can't get the report by the specified path: '{path}'. Invalid response: {r.text}")
            return
        return len(r.json()) + 1

    def generate_report(self, res_uid: str, path: str) -> None | str:
        assert isinstance(path, str), f"Path must be str format, got {type(path)}"

        path_as_list = path.split("/")

        r = self._session.post(
            f"{self.url}/api/report",
            json={
                "reportSpec": {"path": path_as_list, "executorInfo": {"buildName": f"#{path_as_list[-1]}"}},
                "results": [res_uid],
                "deleteResults": True,
            },
        )
        if not r.ok:
            elog(f"Failed to generate report. Invalid response: {r.text}")
            return

        report_url = r.json()["url"]
        return report_url
