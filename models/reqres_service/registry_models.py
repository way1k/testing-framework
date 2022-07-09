from dataclasses import dataclass

from models.reqres_service.endpoint_models.get_api_users import GetApiUsers
from models.reqres_service.endpoint_models.get_api_users_list import GetApiUsersList
from models.reqres_service.endpoint_models.post_api_login import PostApiLogin
from models.reqres_service.endpoint_models.post_api_register import PostApiRegister


@dataclass
class ReqresModels:
    @property
    def get_api_users(self) -> GetApiUsers:
        return GetApiUsers()

    @property
    def post_api_login(self) -> PostApiLogin:
        return PostApiLogin()

    @property
    def post_api_register(self) -> PostApiRegister:
        return PostApiRegister()

    @property
    def get_api_users_list(self) -> GetApiUsersList:
        return GetApiUsersList()
