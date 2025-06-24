from unittest.mock import patch
from uuid import UUID

import pandas as pd
import pytest

from trading_bot_mvp.client.alpaca.generated.alpaca_trading.models.account import (
    Account as AlpacaAccount,
)
from trading_bot_mvp.client.alpaca.generated.alpaca_trading.models.account_status import (
    AccountStatus as AlpacaAccountStatus,
)
from trading_bot_mvp.client.alpaca.generated.alpaca_trading.models.asset_class import AssetClass
from trading_bot_mvp.client.alpaca.generated.alpaca_trading.models.exchange import Exchange
from trading_bot_mvp.client.alpaca.generated.alpaca_trading.models.position import (
    Position as AlpacaPosition,
)
from trading_bot_mvp.service.brokerage.alpaca.alpaca_brokerage_service import (
    AlpacaBrokerageService,
)
from trading_bot_mvp.shared.model import Account, Position


@pytest.fixture
def alpaca_service() -> AlpacaBrokerageService:
    # Use the real client, but all network calls will be patched
    return AlpacaBrokerageService()


def test_get_account_maps_fields(alpaca_service: AlpacaBrokerageService) -> None:
    mock_account_response = AlpacaAccount(
        id=UUID('26201567-9303-4df5-8f8f-a4727d1053a4'),
        status=AlpacaAccountStatus.ACTIVE,
        currency='USD',
        cash='100000',
        equity='100000',
        buying_power='200000',
        created_at=pd.to_datetime('2025-06-20T00:00:00Z'),
    )
    with patch(
        'trading_bot_mvp.service.brokerage.alpaca.alpaca_brokerage_service.get_account',
        return_value=mock_account_response,
    ):
        account = alpaca_service.get_account()
        assert isinstance(account, Account)
        assert account.id == UUID('26201567-9303-4df5-8f8f-a4727d1053a4')
        assert account.status == 'ACTIVE'
        assert account.currency == 'USD'
        assert account.cash == 100000.0
        assert account.equity == 100000.0
        assert account.buying_power == 200000.0
        assert str(account.created_at).startswith('2025-06-20')


def test_get_open_positions_single_symbol(alpaca_service: AlpacaBrokerageService) -> None:
    mock_position_response = AlpacaPosition(
        asset_id=UUID('12345678-1234-5678-1234-567812345678'),
        symbol='AAPL',
        qty='10',
        side='long',
        avg_entry_price='150',
        market_value='1500',
        unrealized_pl='100',
        exchange=Exchange.NYSE,
        asset_class=AssetClass.US_EQUITY,
        qty_available='10',
        cost_basis='400',
        unrealized_plpc='200',
        unrealized_intraday_pl='200',
        unrealized_intraday_plpc='300',
        current_price='400',
        lastday_price='420',
        change_today='69',
        asset_marginable=False,
    )
    with patch(
        'trading_bot_mvp.service.brokerage.alpaca.alpaca_brokerage_service.get_open_position',
        return_value=mock_position_response,
    ):
        positions = alpaca_service.get_open_positions(symbol='AAPL')
        assert isinstance(positions, list)
        assert len(positions) == 1
        assert isinstance(positions[0], Position)
        assert positions[0].symbol == 'AAPL'


def test_get_open_positions_all(alpaca_service: AlpacaBrokerageService) -> None:
    mock_position_response1 = AlpacaPosition(
        asset_id=UUID('12345678-1234-5678-1234-567812345678'),
        symbol='AAPL',
        qty='10',
        side='long',
        avg_entry_price='150',
        market_value='1500',
        unrealized_pl='100',
        exchange=Exchange.NYSE,
        asset_class=AssetClass.US_EQUITY,
        qty_available='10',
        cost_basis='400',
        unrealized_plpc='200',
        unrealized_intraday_pl='200',
        unrealized_intraday_plpc='300',
        current_price='400',
        lastday_price='420',
        change_today='69',
        asset_marginable=False,
    )
    mock_position_response2 = AlpacaPosition(
        asset_id=UUID('12345678-1234-5678-1234-567812345658'),
        symbol='MSFT',
        qty='10',
        side='long',
        avg_entry_price='150',
        market_value='1500',
        unrealized_pl='100',
        exchange=Exchange.NYSE,
        asset_class=AssetClass.US_EQUITY,
        qty_available='10',
        cost_basis='400',
        unrealized_plpc='200',
        unrealized_intraday_pl='200',
        unrealized_intraday_plpc='300',
        current_price='400',
        lastday_price='420',
        change_today='69',
        asset_marginable=False,
    )
    with patch(
        'trading_bot_mvp.service.brokerage.alpaca.alpaca_brokerage_service.get_all_open_positions',
        return_value=[mock_position_response1, mock_position_response2],
    ):
        positions = alpaca_service.get_open_positions()
        assert isinstance(positions, list)
        assert len(positions) == 2
        assert all(isinstance(pos, Position) for pos in positions)
        assert {pos.symbol for pos in positions} == {'AAPL', 'MSFT'}
