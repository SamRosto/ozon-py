from typing import Optional
import httpx


class OzonError(Exception):
    pass


class ApiError(OzonError):
    message: str
    request: httpx.Request
    body: object | None
    code: Optional[str] = None
    param: Optional[str] = None
    typeE: Optional[str] = None
