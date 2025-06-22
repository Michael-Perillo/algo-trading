import pandas as pd
import pytest

from trading_bot_mvp.service.data.alpaca.alpaca_dao import AlpacaDAO
from trading_bot_mvp.shared.mocks.mocks import DummyAPIClient
from trading_bot_mvp.shared.model import BarRequest, Timeframe


@pytest.fixture
def alpaca_dao() -> AlpacaDAO:
    api_client = DummyAPIClient()
    return AlpacaDAO(api_client)


def test_get_bars_returns_dataframe(alpaca_dao: AlpacaDAO) -> None:
    request = BarRequest(symbol='AAPL', timeframe=Timeframe.field_1D, start=None, end=None)
    df = alpaca_dao.get_bars(request)
    assert isinstance(df, pd.DataFrame)
    assert 'symbol' in df.columns
    assert 'open' in df.columns
    assert len(df) == 1
    assert df.iloc[0]['symbol'] == 'AAPL'
    assert df.iloc[0]['open'] == 178.26
