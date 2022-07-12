from requests import Session

from tools.cfg_singleton import ConfigClass, config_obj
from tools.session_singleton import http_session


class ABCService:
    @property
    def session(self) -> Session:
        return http_session()

    @property
    def cfg(self) -> ConfigClass:
        return config_obj
