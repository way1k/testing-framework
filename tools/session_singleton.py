import logging

from requests import Session


class SessionClass:
    _instance = None

    def __call__(self) -> Session:
        if SessionClass._instance is None:
            SessionClass._instance = Session()
            logging.warning("Created new http session instance %X", id(SessionClass._instance))
        return SessionClass._instance

    @classmethod
    def assign_session(cls, session: Session) -> None:
        logging.warning("Assign new http session instance %X", id(session))
        cls._instance = session

    @classmethod
    def close_session(cls) -> None:
        if cls._instance:
            cls.clear_cookies()
            logging.warning("Close http session instance %X", id(cls._instance))
            cls._instance.close()
            del cls._instance
            cls._instance = None

    @classmethod
    def clear_cookies(cls) -> None:
        if cls._instance:
            logging.warning("Clear cookies for http session instance %X", id(cls._instance))
            cls._instance.cookies.clear()


http_session = SessionClass()
