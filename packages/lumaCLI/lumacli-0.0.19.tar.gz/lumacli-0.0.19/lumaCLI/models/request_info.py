from enum import Enum
from typing import Dict, Optional, Tuple, Union

from pydantic import AnyHttpUrl, BaseModel, validator


class HttpMethod(str, Enum):
    GET = "GET"
    POST = "POST"
    PUT = "PUT"
    DELETE = "DELETE"
    HEAD = "HEAD"
    OPTIONS = "OPTIONS"
    PATCH = "PATCH"


class RequestInfo(BaseModel):
    url: AnyHttpUrl
    payload: Optional[Union[Dict, list]]
    verify: bool = True
    method: HttpMethod = HttpMethod.POST
    timeout: Optional[Union[float, Tuple[float, float], Tuple[float, None]]] = (
        3.05,
        60 * 30,
    )
    headers: Optional[Dict[str, str]] = None
    params: Optional[Dict[str, Union[str, int, float]]] = None

    @validator("headers", pre=True, always=True)
    def set_default_headers(cls, v):
        return v or {"Content-Type": "application/json"}

    @validator("method", pre=True)
    def uppercase_method(cls, v):
        return v.upper() if isinstance(v, str) else v
