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


class HeadersModel(pydantic.BaseModel):
    """Валидируемые HTTP заголовки для Ozon API."""

    Client_Id: str = pydantic.Field(..., description="Ozon Client ID")
    Api_Key: str = pydantic.Field(..., description="Ozon API Key")
    Content_Type: Optional[str] = "application/json"

    class Config:
        extra = "allow"

    @pydantic.model_validator(mode="after")
    def validate_headers(self) -> "HeadersModel":
        if not self.Client_Id:
            raise ValueError("Client-Id cannot be empty")
        if not self.Api_Key:
            raise ValueError("Api-Key cannot be empty")
        return self


# HeadersT = Headers | HeadersProtocol
HeadersT = dict[str, str] | HeadersModel
