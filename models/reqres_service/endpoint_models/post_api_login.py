from dataclasses import dataclass

from pydantic import BaseModel, Extra, StrictStr, validator


class PostApiLoginOK(BaseModel, extra=Extra.forbid):
    """Response schema 200 OK /api/login"""

    token: StrictStr


class PostApiLoginBadRequest(BaseModel, extra=Extra.forbid):
    """Response schema 400 Bad Request /api/login"""

    error: StrictStr

    @validator("error")
    def check_len_body(cls, v: dict) -> dict:
        if v != "Missing email or username":
            raise ValueError(f"Expected error message: 'Missing email or username' is not equal actual message: {v}")
        return v


class PostApiLoginNotFound(BaseModel, extra=Extra.forbid):
    """Response schema 404 Not Found /api/login"""

    __root__: dict

    @validator("__root__")
    def check_len_body(cls, v: dict) -> dict:
        if len(v) > 0:
            raise ValueError("Response body is not empty")
        return v


@dataclass
class PostApiLogin:
    """/api/login models registry"""

    ok = PostApiLoginOK
    not_found = PostApiLoginNotFound
    bad_request = PostApiLoginBadRequest
