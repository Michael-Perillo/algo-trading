from unittest.mock import patch

import pytest

from client.client_factory import (
    get_alpaca_data_client,
    get_alpaca_trading_client,
)


def make_settings(api_key: str | None, api_secret: str | None, base_url: str) -> type:
    class Settings:
        APCA_API_KEY_ID = api_key
        APCA_API_SECRET_KEY = api_secret
        APCA_API_BASE_URL = base_url

    return Settings


def test_get_alpaca_trading_client_success() -> None:
    settings = make_settings('key', 'secret', 'https://trading.example.com')
    with (
        patch(
            'client.client_factory.get_alpaca_trading_settings',
            return_value=settings,
        ),
        patch('client.client_factory.AlpacaTradingClient') as MockClient,
    ):
        _ = get_alpaca_trading_client()
        assert MockClient.called
        args, kwargs = MockClient.call_args
        assert kwargs['base_url'] == 'https://trading.example.com'


def test_get_alpaca_trading_client_missing_keys() -> None:
    settings = make_settings(None, None, 'https://trading.example.com')
    with patch('client.client_factory.get_alpaca_trading_settings', return_value=settings):
        with pytest.raises(ValueError):
            get_alpaca_trading_client()


def test_get_alpaca_data_client_success() -> None:
    settings = make_settings('key', 'secret', 'https://data.example.com')
    with (
        patch('client.client_factory.get_alpaca_data_settings', return_value=settings),
        patch('client.client_factory.AlpacaDataClient') as MockClient,
    ):
        _ = get_alpaca_data_client()
        assert MockClient.called
        args, kwargs = MockClient.call_args
        assert kwargs['base_url'] == 'https://data.example.com'


def test_get_alpaca_data_client_missing_keys() -> None:
    settings = make_settings(None, None, 'https://data.example.com')
    with patch('client.client_factory.get_alpaca_data_settings', return_value=settings):
        with pytest.raises(ValueError):
            get_alpaca_data_client()
