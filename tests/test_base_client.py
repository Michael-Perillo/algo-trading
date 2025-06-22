from typing import Any
from unittest.mock import Mock

import httpx
from httpx import Request, Response

from trading_bot_mvp.client.base_client import APIRequest, BaseAPIClient


class DummyAPIClient(BaseAPIClient):
    def __init__(self, mock_json: dict[str, Any] | None = {'result': 'ok'}) -> None:
        mock_client = Mock(spec=httpx.Client)
        dummy_request = Request('GET', 'https://example.com/test')
        mock_response = Response(
            status_code=200,
            json=mock_json,
            headers={'Content-Type': 'application/json'},
            request=dummy_request,
        )
        mock_client.request.return_value = mock_response
        super().__init__(base_url='https://example.com', headers={}, client=mock_client)


def test_api_request_fields() -> None:
    req = APIRequest(method='GET', endpoint='/test', json_data={'foo': 'bar'}, params={'baz': 1})
    assert req.method == 'GET'
    assert req.endpoint == '/test'
    assert req.json_data == {'foo': 'bar'}
    assert req.params == {'baz': 1}


def test_base_api_client_request() -> None:
    client = DummyAPIClient()
    req = APIRequest(method='GET', endpoint='/test')
    resp = client.request(req)
    assert resp.json() == {'result': 'ok'}
