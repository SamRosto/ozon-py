import pydantic
from typing import Literal, Mapping, Protocol, TypeVar

ModelT = TypeVar("ModelT", bound=pydantic.BaseModel)
T = TypeVar("T")
_T = TypeVar("_T")


class Omit:
    def __bool__(self) -> Literal[False]:
        return False


class HeadersProtocol(Protocol):
    def get(self, k: str) -> str | None: ...


omit = Omit()
Omittable = _T | Omit

Headers = Mapping[str, str | omit]
HeadersT = Headers | HeadersProtocol
