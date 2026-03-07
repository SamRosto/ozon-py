import pydantic
from typing import Literal, Mapping, Optional, Protocol, TypeVar, Union


class ClientConfigModel(pydantic.BaseModel):
    client_id: str = pydantic.Field(..., description="Ozon seller Client ID")
    api_key: str = pydantic.Field(..., description="Ozon seller API Key")
    org: Optional[str] = None


ModelT = TypeVar("ModelT", bound=pydantic.BaseModel)
T = TypeVar("T")
_T = TypeVar("_T")


class Omit:
    def __bool__(self) -> Literal[False]:
        return False


omit = Omit()
Omittable = _T | Omit


class HeadersProtocol(Protocol):
    def get(self, k: str) -> str | None: ...


Headers = Mapping[str, Union[str, omit]]

HeadersT = Headers | HeadersProtocol
