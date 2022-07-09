class CommonActionError(Exception):
    """
    Common errors, appearing in UI and API
    """

    def __init__(self, value):
        self.value = value
        super().__init__()

    def __str__(self):
        return "Common error"


class ExecuteSSHCommandError(Exception):
    """
    Error during execute command by ssh
    """

    def __init__(self, stderr_content):
        self.stderr_content = stderr_content
        super().__init__()

    def __str__(self):
        return f"Message received: {self.stderr_content}"
