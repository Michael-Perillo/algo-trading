from httpx import Request, Response

from client.alpaca.generated.alpaca_data.client import (
    Client as AlpacaDataClient,
)
from client.alpaca.generated.alpaca_trading.client import (
    Client as AlpacaTradingClient,
)
from client.alpaca.settings import (
    get_alpaca_data_settings,
    get_alpaca_trading_settings,
)


def log_request(request: Request) -> None:
    print(f'Request event hook: {request.method} {request.url} - Waiting for response')


def log_response(response: Response) -> None:
    request = response.request
    print(f'Response event hook: {request.method} {request.url} - Status {response.status_code}')


httpx_args = {'event_hooks': {'request': [log_request], 'response': [log_response]}}


def get_alpaca_trading_client() -> AlpacaTradingClient:
    """
    Factory for Alpaca Trading API client using settings.
    """
    AlpacaTradingSettings = get_alpaca_trading_settings()
    key_id, key_secret = (
        AlpacaTradingSettings.APCA_API_KEY_ID,
        AlpacaTradingSettings.APCA_API_SECRET_KEY,
    )
    if key_id is None or key_secret is None:
        raise ValueError(
            'Alpaca API key ID and secret key must be set in the environment variables.'
        )
    return AlpacaTradingClient(
        base_url=AlpacaTradingSettings.APCA_API_BASE_URL,
        headers={
            'APCA-API-KEY-ID': key_id,
            'APCA-API-SECRET-KEY': key_secret,
        },
        httpx_args=httpx_args,
    )


def get_alpaca_data_client() -> AlpacaDataClient:
    """
    Factory for Alpaca Data API client using settings.
    """
    AlpacaDataSettings = get_alpaca_data_settings()
    key_id, key_secret = (
        AlpacaDataSettings.APCA_API_KEY_ID,
        AlpacaDataSettings.APCA_API_SECRET_KEY,
    )
    if key_id is None or key_secret is None:
        raise ValueError(
            'Alpaca API key ID and secret key must be set in the environment variables.'
        )
    return AlpacaDataClient(
        base_url=AlpacaDataSettings.APCA_API_BASE_URL,
        headers={
            'APCA-API-KEY-ID': key_id,
            'APCA-API-SECRET-KEY': key_secret,
        },
        httpx_args=httpx_args,
    )
