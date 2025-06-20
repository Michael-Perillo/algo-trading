from uuid import UUID

import pandas as pd
from httpx import Response
import pytest
from unittest.mock import MagicMock

from trading_bot_mvp.client.alpaca.alpaca_client import AlpacaAPIClient
from trading_bot_mvp.service.brokerage.alpaca.alpaca_brokerage_service import AlpacaBrokerageService
from trading_bot_mvp.client.alpaca.trading_models import Account as AlpacaAccountResponseBody
from trading_bot_mvp.shared.model import Account, BarRequest
import trading_bot_mvp.service.brokerage.alpaca.api_field_mappings.model as alpaca_field_mappings

class DummyAPIClient(AlpacaAPIClient):
    def get_account(self):
        return MagicMock(json=lambda: {
  "id": "26201567-9303-4df5-8f8f-a4727d1053a4",
  "admin_configurations": {},
  "user_configurations": None,
  "account_number": "69420",
  "status": "ACTIVE",
  "crypto_status": "ACTIVE",
  "options_approved_level": 2,
  "options_trading_level": 2,
  "currency": "USD",
  "buying_power": "200000",
  "regt_buying_power": "200000",
  "daytrading_buying_power": "0",
  "effective_buying_power": "200000",
  "non_marginable_buying_power": "100000",
  "options_buying_power": "100000",
  "bod_dtbp": "0",
  "cash": "100000",
  "accrued_fees": "0",
  "portfolio_value": "100000",
  "pattern_day_trader": False,
  "trading_blocked": False,
  "transfers_blocked": False,
  "account_blocked": False,
  "created_at": "2025-06-20T15:13:44.139591Z",
  "trade_suspended_by_user": False,
  "multiplier": "2",
  "shorting_enabled": True,
  "equity": "100000",
  "last_equity": "100000",
  "long_market_value": "0",
  "short_market_value": "0",
  "position_market_value": "0",
  "initial_margin": "0",
  "maintenance_margin": "0",
  "last_maintenance_margin": "0",
  "sma": "0",
  "daytrade_count": 0,
  "balance_asof": "2025-06-18",
  "crypto_tier": 0,
  "intraday_adjustments": "0",
  "pending_reg_taf_fees": "0"
})

    def get_bars(self, symbols: str, start: str = None, end: str = None, timeframe: str = None, limit: int = None, page_token: str = None, adjustment: str = None, feed: str = None):
        # Simulate a paginated Alpaca API response for bars
        class DummyResponse(Response):
            def json(self_inner):
                return {
  "bars": {
    "AAPL": [
      {
        "t": "2022-01-03T09:00:00Z",
        "o": 178.26,
        "h": 178.26,
        "l": 178.21,
        "c": 178.21,
        "v": 1118,
        "n": 65,
        "vw": 178.235733
      }
    ]
  },
  "next_page_token": None
}
        return DummyResponse(status_code=200)

@pytest.fixture
def alpaca_service():
    api_client = DummyAPIClient()
    return AlpacaBrokerageService(api_client)

def test_get_account_maps_fields(alpaca_service):
    account = alpaca_service.get_account()
    assert isinstance(account, Account)
    assert account.id == UUID("26201567-9303-4df5-8f8f-a4727d1053a4")
    assert account.status == "ACTIVE"
    assert account.currency == "USD"
    assert account.cash == 100000
    assert account.equity == 100000
    assert account.buying_power == 200000
    assert str(account.created_at).startswith("2025-06-20")

def test_get_bars_returns_dataframe(alpaca_service):
    request = BarRequest(symbol="AAPL", timeframe="1d")
    df = alpaca_service.get_bars(request)
    assert isinstance(df, pd.DataFrame)
    assert "symbol" in df.columns
    assert "o" in df.columns
    assert len(df) == 1
    assert df.iloc[0]["symbol"] == "AAPL"
    assert df.iloc[0]["o"] == 178.26
    assert df.index.name == "t"
