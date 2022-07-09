import logging
from time import sleep, time

from paramiko import AutoAddPolicy, SSHClient

from tools.custom_exeptions import ExecuteSSHCommandError


class SSH:
    """
    Ssh client
    """

    def __init__(self, hostname: str, username: str, password: str | None = None) -> None:
        self._ssh_client = SSHClient()
        self._ssh_client.set_missing_host_key_policy(AutoAddPolicy())
        self._ssh_client.load_system_host_keys()
        self._ssh_client.connect(hostname=hostname, username=username, password=password)

    def run_command(
        self, command: str, timeout: int = 120, first_result: bool = False
    ) -> tuple[str | list, str | list]:
        _, stdout, stderr = self._ssh_client.exec_command(command=command, timeout=timeout)
        end_time = time() + timeout

        while not stdout.channel.eof_received:
            sleep(1)
            if time() > end_time:
                stdout.channel.close()
                break

        out_format = stdout.read().decode()
        out_result = out_format.split("\n")

        error_format = stderr.read().decode()
        error_result = error_format.split("\n")

        logging.info(f"Command executed: '{command}'")

        if first_result:
            return out_result[0], error_result[0]
        else:
            return out_result, error_result

    """
    Application process methods
    """

    def service_statuses(self, service: str) -> str:
        status_stdout, status_error = self.run_command(
            command="supervisorctl status | awk " + f"'/{service}/" + ' {print $1, "status "$2, $3, $4}\'', timeout=20
        )
        if len(status_error) > 1:
            raise ExecuteSSHCommandError(stderr_content=status_error)
        return status_stdout

    def _convert_status(self, stdout: list):
        service_key = []
        status_values = []

        formatted_stdout = filter(None, [x.replace(",", "") for x in stdout])
        formatted_stdout = [x.split(" ") for x in formatted_stdout]

        for service in formatted_stdout:
            service_key.append(service.pop(0))

        for statuses in formatted_stdout:
            status = dict(zip(statuses[::2], statuses[1::2]))
            status_values.append(status.copy())

        return dict(zip(service_key, status_values))

    def restart_service_processes(self, service: str):
        service_statuses = self.service_statuses(service)
        process_list = self._convert_status(service_statuses)
        for process in process_list.keys():
            restart_stdout, restart_error = self.run_command(command=f"supervisorctl restart {process}", timeout=20)
            logging.debug(f"Received response: {restart_stdout}")
            if len(restart_error) > 1:
                raise ExecuteSSHCommandError(stderr_content=restart_error)
