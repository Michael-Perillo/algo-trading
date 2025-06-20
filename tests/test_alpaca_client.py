import pytest
from trading_bot_mvp.client.alpaca.alpaca_client import AlpacaAPIClient
from trading_bot_mvp.client.base_client import APIRequest

class DummyAlpacaAPIClient(AlpacaAPIClient):
    def __init__(self):
        super().__init__(base_url="https://example.com", headers={})
        self.last_request = None
    def request(self, req: APIRequest) -> dict:
        self.last_request = req
        return {"bars": [{"t": "2024-01-01T00:00:00Z", "o": 1, "h": 2, "l": 0.5, "c": 1.5, "v": 100}]}

def test_get_bars():
    client = DummyAlpacaAPIClient()
    resp = client.get_bars(symbols="AAPL", timeframe="1Day")
    assert "bars" in resp
    assert isinstance(resp["bars"], list)
    assert client.last_request.endpoint == "/v2/stocks/bars"
    assert client.last_request.params["symbols"] == "AAPL"
    assert client.last_request.params["timeframe"] == "1Day"

