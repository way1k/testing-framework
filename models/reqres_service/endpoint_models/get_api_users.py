from dataclasses import dataclass

from pydantic import BaseModel, EmailStr, Extra, Field, HttpUrl, StrictInt, StrictStr, validator


class Data(BaseModel, extra=Extra.forbid):
    id: StrictInt
    email: EmailStr
    first_name: StrictStr
    last_name: StrictStr
    avatar: HttpUrl


class Support(BaseModel, extra=Extra.forbid):
    url: HttpUrl
    text: StrictStr = Field("To keep ReqRes free, contributions towards server costs are appreciated!", const=True)


class GetApiUsersOK(BaseModel, extra=Extra.forbid):
    """Response schema 200 OK /api/users/{user_id}"""

    data: Data
    support: Support


class GetApiUsersBadRequest(BaseModel, extra=Extra.forbid):
    """Response schema 400 Bad Request /api/users/{user_id}"""

    __root__: dict

    @validator("__root__")
    def check_len_body(cls, v: dict) -> dict:
        if len(v) > 0:
            raise ValueError("Response body is not empty")
        return v


class GetApiUsersNotFound(BaseModel, extra=Extra.forbid):
    """Response schema 404 Not Found /api/users/{user_id}"""

    __root__: dict

    @validator("__root__")
    def check_len_body(cls, v: dict) -> dict:
        if len(v) > 0:
            raise ValueError("Response body is not empty")
        return v


@dataclass
class GetApiUsers:
    """/api/users/{user_id} models registry"""

    ok = GetApiUsersOK
    not_found = GetApiUsersNotFound
    bad_request = GetApiUsersBadRequest
