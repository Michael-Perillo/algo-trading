import hishel
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
    if response.status_code != 200:
        # Decode bytes to string for printing
        error_content = response.read()
        if isinstance(error_content, str):
            print(f'Error response: {error_content}')
        elif isinstance(error_content, bytes):
            print(f'Error response: {error_content.decode(errors="replace")}')
        else:
            print(f'Error response: {str(error_content)}')


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
    # Use hishel for in-memory caching
    hishel_client = hishel.CacheClient(
        base_url=AlpacaTradingSettings.APCA_API_BASE_URL,
        headers={
            'APCA-API-KEY-ID': key_id,
            'APCA-API-SECRET-KEY': key_secret,
        },
        event_hooks={'request': [log_request], 'response': [log_response]},
        storage=hishel.InMemoryStorage(),
    )
    return AlpacaTradingClient(base_url=AlpacaTradingSettings.APCA_API_BASE_URL).set_httpx_client(
        hishel_client
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
    # Use hishel.CacheClient for in-memory caching
    hishel_cache_client = hishel.CacheClient(
        event_hooks={'request': [log_request], 'response': [log_response]},
        base_url=AlpacaDataSettings.APCA_API_BASE_URL,
        headers={
            'APCA-API-KEY-ID': key_id,
            'APCA-API-SECRET-KEY': key_secret,
        },
        storage=hishel.InMemoryStorage(),
    )
    return AlpacaDataClient(base_url=AlpacaDataSettings.APCA_API_BASE_URL).set_httpx_client(
        hishel_cache_client
    )
