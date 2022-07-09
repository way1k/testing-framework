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


class GetApiUsersListOK(BaseModel, extra=Extra.forbid):
    """Response schema 200 OK /api/users?page={page_number}"""

    page: StrictInt
    per_page: StrictInt
    total: StrictInt
    total_pages: StrictInt
    data: list[Data]
    support: Support


class GetApiUsersListBadRequest(BaseModel, extra=Extra.forbid):
    """Response schema 400 Bad Request /api/users?page={page_number}"""

    __root__: dict

    @validator("__root__")
    def check_len_body(cls, v: dict) -> dict:
        if len(v) > 0:
            raise ValueError("Response body is not empty")
        return v


class GetApiUsersListNotFound(BaseModel, extra=Extra.forbid):
    """Response schema 404 Not Found /api/users?page={page_number}"""

    __root__: dict

    @validator("__root__")
    def check_len_body(cls, v: dict) -> dict:
        if len(v) > 0:
            raise ValueError("Response body is not empty")
        return v


@dataclass
class GetApiUsersList:
    """/api/users?page={page_number} models registry"""

    ok = GetApiUsersListOK
    not_found = GetApiUsersListNotFound
    bad_request = GetApiUsersListBadRequest
