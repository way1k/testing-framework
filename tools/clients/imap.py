from imap_tools import MailBox
from imap_tools import A
from time import sleep


class IMAPClient:
    """
    Класс клиента подключения к почтовому серверу
    """

    def __init__(self, host, username, password, port=993, initial_folder='INBOX'):
        self.mailbox = MailBox(host=host, port=port)
        self.mailbox.login(
            username=username,
            password=password,
            initial_folder=initial_folder)

    def logout(self):
        self.mailbox.logout()

    def get_text_in_mail_body(self, expected_text: str):
        mail_query = [msg.text for msg in self.mailbox.fetch(A(
            text=f"{expected_text}"),
            charset='utf8')]
        return self.__fetch_mail_query(mail_query)

    def get_send_to_mails(self, send_to: str or list):
        mail_query = [msg.to for msg in self.mailbox.fetch(A(
            text=f"{send_to}"),
            charset='utf8')]
        return self.__fetch_mail_query(mail_query)

    @staticmethod
    def __fetch_mail_query(mail_query: str or list, wait_retries: int = 5, retries_delay: int = 5):
        actual_retries = 0
        while 1:
            result = mail_query
            if result == {} or result == [] or result is None:
                actual_retries += 1
                if actual_retries == wait_retries:
                    raise AssertionError(f"Запрос в почтовый сервис '{mail_query}' возвращает пустой ответ")
                sleep(retries_delay)
            else:
                return result
