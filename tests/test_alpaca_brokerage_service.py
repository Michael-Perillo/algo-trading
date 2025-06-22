from uuid import UUID

import pytest

from trading_bot_mvp.service.brokerage.alpaca.alpaca_brokerage_service import (
    AlpacaBrokerageService,
)
from trading_bot_mvp.shared.mocks.mocks import DummyAPIClient
from trading_bot_mvp.shared.model import Account, Position


@pytest.fixture
def alpaca_service() -> AlpacaBrokerageService:
    api_client = DummyAPIClient()
    return AlpacaBrokerageService(api_client)


def test_get_account_maps_fields(alpaca_service: AlpacaBrokerageService) -> None:
    account = alpaca_service.get_account()
    assert isinstance(account, Account)
    assert account.id == UUID('26201567-9303-4df5-8f8f-a4727d1053a4')
    assert account.status == 'ACTIVE'
    assert account.currency == 'USD'
    assert account.cash == 100000
    assert account.equity == 100000
    assert account.buying_power == 200000
    assert str(account.created_at).startswith('2025-06-20')


def test_get_open_positions_single_symbol(alpaca_service: AlpacaBrokerageService) -> None:
    positions = alpaca_service.get_open_positions(symbol='AAPL')
    assert isinstance(positions, list)
    assert len(positions) == 1
    assert isinstance(positions[0], Position)
    assert positions[0].symbol == 'AAPL'


def test_get_open_positions_all(alpaca_service: AlpacaBrokerageService) -> None:
    positions = alpaca_service.get_open_positions()
    assert isinstance(positions, list)
    assert len(positions) == 2
    assert all(isinstance(pos, Position) for pos in positions)
    assert {pos.symbol for pos in positions} == {'AAPL', 'MSFT'}
