import pytest
from trading_bot_mvp.client.base_client import BaseAPIClient, APIRequest

class DummyAPIClient(BaseAPIClient):
    def __init__(self):
        super().__init__(base_url="https://example.com", headers={})
        self.last_request = None
    def request(self, req: APIRequest) -> dict:
        self.last_request = req
        return {"result": "ok"}

def test_api_request_fields():
    req = APIRequest(method="GET", endpoint="/test", json_data={"foo": "bar"}, params={"baz": 1})
    assert req.method == "GET"
    assert req.endpoint == "/test"
    assert req.json_data == {"foo": "bar"}
    assert req.params == {"baz": 1}

def test_base_api_client_request():
    client = DummyAPIClient()
    req = APIRequest(method="GET", endpoint="/test")
    resp = client.request(req)
    assert resp == {"result": "ok"}
    assert client.last_request == req

