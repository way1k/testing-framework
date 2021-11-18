class CommonActionError(Exception):
    """
    Общие ошибки, возникающие в UI и API
    """

    def __init__(self, value):
        self.value = value
        super().__init__()

    def __str__(self):
        return "Общая ошибка"


class ExecuteSSHCommandError(Exception):
    """
    Ошибки при выполнении команд по ssh
    """

    def __init__(self, stderr_content):
        self.stderr_content = stderr_content
        super().__init__()

    def __str__(self):
        return f"Получено сообщение {self.stderr_content}"
