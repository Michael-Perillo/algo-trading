import httpx
from pydantic import BaseModel
from abc import ABC
from typing import Optional, Dict, Any
from trading_bot_mvp.settings import get_settings


class APIRequest(BaseModel):
    method: str
    endpoint: str
    json_data: Optional[Dict[str, Any]] = None
    params: Optional[Dict[str, Any]] = None


class BaseAPIClient(ABC):
    """
    Simple HTTP client for making authenticated requests to an API.
    Handles authentication and returns raw JSON/dict responses.
    """

    def __init__(self, base_url: Optional[str] = None, headers: Optional[dict] = None):
        settings = get_settings()
        self._base_url = base_url or settings.BASE_URL
        self._headers = headers or {
            'Content-Type': 'application/json',
        }
        self._client = httpx.Client(
            base_url=self._base_url, headers=self._headers, timeout=10.0
        )

    def request(self, req: APIRequest) -> httpx.Response:
        """Make an HTTP request and return the raw JSON response."""
        response = self._client.request(
            method=req.method,
            headers=self._headers,
            url=req.endpoint,
            json=req.json_data,
            params=req.params,
        )
        response.raise_for_status()
        return response
