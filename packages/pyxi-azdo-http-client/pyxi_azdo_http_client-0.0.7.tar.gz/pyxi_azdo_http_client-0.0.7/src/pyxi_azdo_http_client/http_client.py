import httpx
from typing import Optional


class HttpClient:
    def get(self, url: str, headers: Optional[dict[str, str]] = None):
        with self.create_client() as client:
            return client.get(url, headers=headers)

    def post(
        self, url: str, json: dict[str, str], headers: Optional[dict[str, str]] = None
    ):
        with self.create_client() as client:
            return client.post(url, headers=headers, json=json)

    def create_client(self) -> httpx.Client:
        return httpx.Client(verify=False)
