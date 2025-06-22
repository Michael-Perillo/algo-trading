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
        if req.endpoint == '/v2/account':
            return self._mock_account_response()
        elif req.endpoint == '/v2/positions':
            return self._mock_positions_response(symbol=None)
        # if the request matches /v2/positions/{symbol}, we return a single position
        elif req.endpoint.startswith('/v2/positions/'):
            symbol = req.endpoint.split('/')[-1]
            return self._mock_positions_response(symbol=symbol)
        else:
            raise ValueError(f'Unknown endpoint: {req.endpoint}')

    def _mock_account_response(self) -> Response:
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

    def _mock_positions_response(self, symbol: str | None) -> Response:
        if symbol:
            return Response(
                status_code=200,
                headers={'Content-Type': 'application/json'},
                json={
                    'asset_id': '26201567-9303-4df5-8f8f-a4727d1053a4',
                    'symbol': symbol,
                    'exchange': 'NYSE',
                    'asset_class': 'us_equity',
                    'qty': '10',
                    'qty_available': '10',
                    'side': 'long',
                    'avg_entry_price': '100.0',
                    'market_value': '1000.0',
                    'cost_basis': '1000.0',
                    'unrealized_pl': '0.0',
                    'unrealized_plpc': '0.0',
                    'unrealized_intraday_pl': '0.0',
                    'unrealized_intraday_plpc': '0.0',
                    'current_price': '100.0',
                    'lastday_price': '99.0',
                    'change_today': '0.01',
                    'asset_marginable': True,
                },
            )
        else:
            # Return a list of positions
            # json should be a list of position dicts
            mock_positions = [
                {
                    'asset_id': '26201567-9303-4df5-8f8f-a4727d1053a4',
                    'symbol': 'AAPL',
                    'exchange': 'NYSE',
                    'asset_class': 'us_equity',
                    'qty': '10',
                    'qty_available': '10',
                    'side': 'long',
                    'avg_entry_price': '100.0',
                    'market_value': '1000.0',
                    'cost_basis': '1000.0',
                    'unrealized_pl': '0.0',
                    'unrealized_plpc': '0.0',
                    'unrealized_intraday_pl': '0.0',
                    'unrealized_intraday_plpc': '0.0',
                    'current_price': '100.0',
                    'lastday_price': '99.0',
                    'change_today': '0.01',
                    'asset_marginable': True,
                },
                {
                    'asset_id': '26201567-9303-4df5-8f8f-a4727d1053a4',
                    'symbol': 'MSFT',
                    'exchange': 'NASDAQ',
                    'asset_class': 'us_equity',
                    'qty': '5',
                    'qty_available': '5',
                    'side': 'long',
                    'avg_entry_price': '200.0',
                    'market_value': '1000.0',
                    'cost_basis': '1000.0',
                    'unrealized_pl': '0.0',
                    'unrealized_plpc': '0.0',
                    'unrealized_intraday_pl': '0.0',
                    'unrealized_intraday_plpc': '0.0',
                    'current_price': '200.0',
                    'lastday_price': '198.0',
                    'change_today': '0.01',
                    'asset_marginable': True,
                },
            ]
            # the response body is a list of objects
            # use the list of dicts as the json response
            return Response(
                status_code=200,
                headers={'Content-Type': 'application/json'},
                json=mock_positions,
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


def test_get_positions() -> None:
    client = make_dummy_api_client()
    resp = client.get_open_positions()
    data = resp.json()
    assert resp.status_code == 200
    assert isinstance(data, list)
    assert len(data) > 0
    assert all('symbol' in pos for pos in data)
    assert client.last_request is not None
    assert client.last_request.endpoint == '/v2/positions'


def test_get_position_by_symbol() -> None:
    client = make_dummy_api_client()
    resp = client.get_open_positions('AAPL')
    data = resp.json()
    assert resp.status_code == 200
    assert data['symbol'] == 'AAPL'
    assert client.last_request is not None
    assert client.last_request.endpoint == '/v2/positions/AAPL'
