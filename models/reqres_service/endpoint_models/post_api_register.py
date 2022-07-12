from dataclasses import dataclass

from pydantic import BaseModel, Extra, StrictInt, StrictStr, validator


class PostApiRegisterOK(BaseModel, extra=Extra.forbid):
    """Response schema 200 OK /api/register"""

    id: StrictInt
    token: StrictStr


class PostApiRegisterBadRequest(BaseModel, extra=Extra.forbid):
    """Response schema 400 Bad Request /api/register"""

    __root__: dict

    @validator("__root__")
    def check_len_body(cls, v: dict) -> dict:
        if len(v) > 0:
            raise ValueError("Response body is not empty")
        return v


class PostApiRegisterNotFound(BaseModel, extra=Extra.forbid):
    """Response schema 404 Not Found /api/register"""

    __root__: dict

    @validator("__root__")
    def check_len_body(cls, v: dict) -> dict:
        if len(v) > 0:
            raise ValueError("Response body is not empty")
        return v


@dataclass
class PostApiRegister:
    """/api/register models registry"""

    ok = PostApiRegisterOK
    not_found = PostApiRegisterNotFound
    bad_request = PostApiRegisterBadRequest
