from services.reqres_service.helpers.get_api_users import GetApiUsers
from services.reqres_service.helpers.get_api_users_list import GetApiUsersList
from services.reqres_service.helpers.post_api_register import PostApiRegister
from services.reqres_service.helpers.post_create_api_users import PostCreateApiUsers


class ReqresHelpers:
    """reqres service helpers methods"""

    @property
    def get_api_users(self) -> GetApiUsers:
        return GetApiUsers()

    @property
    def get_api_users_list(self) -> GetApiUsersList:
        return GetApiUsersList()

    @property
    def post_api_register(self) -> PostApiRegister:
        return PostApiRegister()

    @property
    def post_create_api_users(self) -> PostCreateApiUsers:
        return PostCreateApiUsers()
