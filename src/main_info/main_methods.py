import httpx
import pydantic

from urllib.parse import urljoin
from src._utils import parse_url_endpoint
from src._types import HeadersT


class ApiUrl(pydantic.BaseModel):
    base_url: str
    endpoint: str

    def full_url(self) -> str:
        # return super().model_post_init(context)
        return urljoin(self.base_url, self.endpoint)


class ApiMethod(pydantic.BaseModel):
    path: str


class ApiRole(pydantic.BaseModel):
    name: str
    methods: list[str]


class ApiKeyRolesResponse(pydantic.BaseModel):
    """Полный ответ от /api-key-roles."""

    roles: list[ApiRole]
    expires_at: str | None


class ApiKeyRoles:
    """
    Получение информации и ролях и методах, привязанных к API-ключу.
    """

    endpoint = "/v1/roles"
    timeout = httpx.Timeout(10.0, read=30.0)

    @classmethod
    def get_settings(cls, base_url: str, headers: HeadersT):
        parsed_endpoint = parse_url_endpoint(ApiKeyRoles.endpoint)
        api_url = ApiUrl(base_url=base_url, endpoint=parsed_endpoint)

        with httpx.Client(timeout=ApiKeyRoles.timeout) as http_client:
            response = http_client.post(
                url=api_url.full_url(),
                headers=headers,
                json={},
            )
            response.raise_for_status()

            data = response.json()
            return ApiKeyRolesResponse.model_validate(data)
