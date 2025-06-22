from httpx import Response

from trading_bot_mvp.client.alpaca.alpaca_client import (
    AlpacaAPIClient,
    AlpacaDataClient,
)
from trading_bot_mvp.client.base_client import APIRequest


class DummyDataClient(AlpacaDataClient):
    def __init__(self) -> None:
        super().__init__(base_url='https://example.com', headers={})
        self.last_request: APIRequest | None = None

    def request(self, req: APIRequest) -> Response:
        self.last_request = req
        bars_body = {
            'bars': {
                'AAPL': [
                    {
                        't': '2022-01-03T09:00:00Z',
                        'o': 178.26,
                        'h': 178.26,
                        'l': 178.21,
                        'c': 178.21,
                        'v': 1118,
                        'n': 65,
                        'vw': 178.235733,
                    }
                ]
            },
            'next_page_token': None,
        }
        return Response(
            status_code=200, json=bars_body, headers={'Content-Type': 'application/json'}
        )


class DummyAPIClient(AlpacaAPIClient):
    def __init__(self) -> None:
        super().__init__(base_url='https://example.com', headers={})
        self.last_request: APIRequest | None = None

    def request(self, req: APIRequest) -> Response:
        self.last_request = req
        account_body = {
            'id': 'dummy',
            'status': 'ACTIVE',
            'currency': 'USD',
            'buying_power': '10000',
            'cash': '5000',
            'equity': '15000',
        }
        return Response(
            status_code=200, json=account_body, headers={'Content-Type': 'application/json'}
        )


# Dummy client for AlpacaDataClient
def make_dummy_data_client() -> DummyDataClient:
    return DummyDataClient()


# Dummy client for AlpacaAPIClient
def make_dummy_api_client() -> DummyAPIClient:
    return DummyAPIClient()


def test_get_bars() -> None:
    client = make_dummy_data_client()
    resp = client.get_bars(symbols='AAPL', timeframe='1D')
    assert 'bars' in resp.json()
    assert client.last_request is not None
    assert client.last_request.endpoint == '/v2/stocks/bars'
    assert client.last_request.params is not None
    assert client.last_request.params.get('symbols') == 'AAPL'
    assert client.last_request.params.get('timeframe') == '1D'


def test_get_account() -> None:
    client = make_dummy_api_client()
    resp = client.get_account()
    data = resp.json()
    assert resp.status_code == 200
    assert data['status'] == 'ACTIVE'
    assert data['currency'] == 'USD'
    assert data['buying_power'] == '10000'
    assert data['cash'] == '5000'
    assert data['equity'] == '15000'
    assert client.last_request is not None
    assert client.last_request.endpoint == '/v2/account'
