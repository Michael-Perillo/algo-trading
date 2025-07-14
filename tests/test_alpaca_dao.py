from unittest.mock import MagicMock, patch

import pandas as pd
import pytest

from service.data.alpaca.alpaca_dao import AlpacaDAO
from shared.model import BarRequest, Timeframe


@pytest.fixture
def alpaca_dao() -> AlpacaDAO:
    # Inject a MagicMock to prevent real network calls
    return AlpacaDAO(api_client=MagicMock())


def make_bars_response() -> MagicMock:
    # Mock a StockBarsResp with the structure expected by parse_bars_response
    bar = {
        't': pd.Timestamp('2024-06-20T00:00:00Z'),
        'o': 178.26,
        'h': 180.0,
        'l': 177.5,
        'c': 179.0,
        'v': 1000,
    }
    bars = {'AAPL': [bar]}
    bars_resp = MagicMock()
    bars_resp.bars.to_dict.return_value = bars
    bars_resp.next_page_token = None  # Ensure pagination ends
    return bars_resp


def test_get_bars_returns_dataframe(alpaca_dao: AlpacaDAO) -> None:
    request = BarRequest(symbol='AAPL', timeframe=Timeframe.field_1D, start=None, end=None)
    bars_response = make_bars_response()
    # Patch at the location where stock_bars.sync is imported/used in AlpacaDAO
    with patch('service.data.alpaca.alpaca_dao.get_stock_bars', autospec=True) as mock_stock_bars:
        mock_stock_bars.return_value = bars_response
        df = alpaca_dao.get_bars(request)
        assert isinstance(df, pd.DataFrame)
        assert 'symbol' in df.columns
        assert 'open' in df.columns
        assert len(df) == 1
        assert df.iloc[0]['symbol'] == 'AAPL'
        assert df.iloc[0]['open'] == 178.26


def test_get_bars_raises_on_none_response(alpaca_dao: AlpacaDAO) -> None:
    request = BarRequest(symbol='AAPL', timeframe=Timeframe.field_1D, start=None, end=None)
    with patch('service.data.alpaca.alpaca_dao.get_stock_bars', return_value=None):
        with pytest.raises(ValueError, match='Failed to fetch bars from Alpaca'):
            alpaca_dao.get_bars(request)
