from typing import Optional

from dotenv import load_dotenv
import os

from src._utils import BaseOzonClient
from src.main_info.main_methods import ApiKeyRoles

from ._types import ClientConfigModel, HeadersT


class OzonClient(BaseOzonClient):
    def __init__(self, *, config: Optional[ClientConfigModel] = None) -> None:
        try:
            load_dotenv()
        except Exception as e:
            print(f"Warning: Could not load .env file: {e}")

        if config is None:
            config = self._load_from_env()

        self.config = config
        self.client_id = config.client_id
        self.api_key = config.api_key
        self.org = config.org
        self.headers = self._get_headers()

        super().__init__()

        self._check_roles()

    def _load_from_env(self) -> ClientConfigModel:
        client_id = os.getenv("CLIENT_ID") or os.getenv("CLIENT-ID")
        api_key = os.getenv("API_KEY") or os.getenv("API-KEY")
        org = os.getenv("ORG")

        if not api_key:
            raise KeyError("Please provide Ozon seller API Key (API_KEY or env)")
        if not client_id:
            raise KeyError(
                "Please provide Ozon seller Client Id (CLIENT_ID or CLIENT-ID)"
            )

        return ClientConfigModel(client_id=client_id, api_key=api_key, org=org)

    def _get_headers(self) -> HeadersT:
        return {
            "Client-Id": self.client_id,
            "Api-Key": self.api_key,
            "Content-Type": "application/json",
        }

    @classmethod
    def from_env(cls) -> "OzonClient":
        """
        Create from .env
        Same as: client = OzonClient()
        """
        return cls()

    @classmethod
    def from_config(
        cls, client_id: str, api_key: str, org: Optional[str] = None
    ) -> "OzonClient":
        """
        Create from params.
        client = OzonClient.from_`config(
            client_id="12345",
            api_key="your-api-key",
            org="org_1"
        )
        """
        config = ClientConfigModel(client_id=client_id, api_key=api_key, org=org)
        return cls(config=config)

    def __repr__(self) -> str:
        return f"OzonClient(client_id='{self.client_id}', api_key='***{self.api_key[-4:]}')\nheaders={self.headers}"

    def _check_roles(self):
        settings = ApiKeyRoles.get_settings(
            base_url=self.base_url, headers=self.headers
        )

        for role in settings.roles:
            self.role_name = role.name
            role_methods = role.methods
            self._available_methods.extend(role_methods)  # добавляем в список

        # return settings

    @property
    def available_methods(self):
        """Отобоажает список доступеых методов по API ключу"""
        # return [m for m in self.available_methods]
        return self._available_methods
