from tools.abc_service import ABCService
from tools.clients.endpoint import Endpoint


class ReqresEndpoints(ABCService):
    """reqres service endpoints"""

    get_api_users = Endpoint(method="get", url="/api/users/{user_id}")

    post_api_register = Endpoint(method="post", url="/api/register")

    post_api_login = Endpoint(method="post", url="/api/login")

    post_create_api_users = Endpoint(method="post", url="/api/users")

    get_api_users_list = Endpoint(method="get", url="/api/users")
