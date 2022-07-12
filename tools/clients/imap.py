from time import sleep

from imap_tools import A, MailBox


class IMAPClient:
    """
    Client for connection to mail server
    """

    def __init__(self, host: str, username: str, password: str, port: int = 993, initial_folder: str = "INBOX") -> None:
        self.mailbox = MailBox(host=host, port=port)
        self.mailbox.login(username=username, password=password, initial_folder=initial_folder)

    def logout(self) -> None:
        self.mailbox.logout()

    def get_text_in_mail_body(self, expected_text: str) -> list:
        mail_query = [msg.text for msg in self.mailbox.fetch(A(text=f"{expected_text}"), charset="utf8")]
        return self.__fetch_mail_query(mail_query)

    def get_send_to_mails(self, send_to: str | list) -> list:
        mail_query = [msg.to for msg in self.mailbox.fetch(A(text=f"{send_to}"), charset="utf8")]
        return self.__fetch_mail_query(mail_query)

    @staticmethod
    def __fetch_mail_query(mail_query: str | list, wait_retries: int = 5, retries_delay: int = 5) -> list:
        actual_retries = 0
        while 1:
            result = mail_query
            if result == {} or result == [] or result is None:
                actual_retries += 1
                if actual_retries == wait_retries:
                    raise AssertionError(f"Request to mail service '{mail_query}' receive empty response")
                sleep(retries_delay)
            else:
                return result
