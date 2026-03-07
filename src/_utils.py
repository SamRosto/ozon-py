def parse_url_endpoint(path: str):
    return path if path.startswith("/") else path.lstrip("/")


class BaseOzonClient:
    def __init__(self):
        self.base_url = "https://api-seller.ozon.ru".rstrip("/")
        # url if not url.endswith("/") else url.rstrip("/")
        self._available_methods: list[str | None] = []
