from uuid import UUID

import pandas as pd
import pytest

from trading_bot_mvp.service.brokerage.alpaca.alpaca_brokerage_service import (
    AlpacaBrokerageService,
)
from trading_bot_mvp.shared.model import Account, BarRequest
from trading_bot_mvp.shared.mocks.mocks import DummyAPIClient


@pytest.fixture
def alpaca_service():
    api_client = DummyAPIClient()
    return AlpacaBrokerageService(api_client)


def test_get_account_maps_fields(alpaca_service):
    account = alpaca_service.get_account()
    assert isinstance(account, Account)
    assert account.id == UUID('26201567-9303-4df5-8f8f-a4727d1053a4')
    assert account.status == 'ACTIVE'
    assert account.currency == 'USD'
    assert account.cash == 100000
    assert account.equity == 100000
    assert account.buying_power == 200000
    assert str(account.created_at).startswith('2025-06-20')
