from . import omit

from dotenv import load_dotenv
import os


class OzonClient:
    client_id: str
    api_key: str
    org: str | None

    def __init__(
        self,
        *,
        client_id: str | None = None,
        api_key: str | None = None,
        org: str | None = None,
    ) -> None:
        try:
            load_dotenv()
        except Exception as e:
            print(f"Warning: Could not load .env file: {e}")

        if api_key is None:
            api_key = os.getenv("API_KEY")
            self.api_key = api_key
        if api_key is None:
            raise KeyError("Please provide Ozon seller API Key")

        if client_id is None:
            client_id = os.getenv("CLIENT-ID")
            self.client_id = client_id
        if client_id is None:
            raise KeyError("Please provide Ozon seller Client Id")

        if org is None:
            org = os.getenv("ORG")
        self.org = org
