from unittest.mock import MagicMock

import pandas as pd
import pytest
from pandera.typing.pandas import DataFrame

from client.alpaca.adapters import alpaca_bars_column_mapping as standard_mapping
from service.data.bars_column_models import BarsSchema
from service.data.base_dao import BaseDAO
from shared.model import BarRequest, Timeframe


class DummyDAO(BaseDAO):
    def __init__(self, api_client: None = None) -> None:
        super().__init__(MagicMock())

    def get_bars(self, request: BarRequest) -> DataFrame[BarsSchema]:
        raw_df = pd.DataFrame(
            [
                {
                    't': '2022-01-03T09:00:00Z',
                    'o': 100.0,
                    'h': 110.0,
                    'l': 90.0,
                    'c': 105.0,
                    'v': 1000,
                    'symbol': 'AAPL',
                },
                {
                    't': '2022-01-04T09:00:00Z',
                    'o': 105.0,
                    'h': 115.0,
                    'l': 95.0,
                    'c': 110.0,
                    'v': 1200,
                    'symbol': 'AAPL',
                },
            ]
        )
        return self.standardize_bars_dataframe(raw_df, standard_mapping())


@pytest.fixture
def dummy_dao() -> DummyDAO:
    return DummyDAO()


@pytest.fixture
def bar_request() -> BarRequest:
    return BarRequest(symbol='AAPL', timeframe=Timeframe.field_1D, start=None, end=None)


def test_standardize_bars_dataframe(dummy_dao: DummyDAO, bar_request: BarRequest) -> None:
    std_df = dummy_dao.get_bars(bar_request)
    assert list(std_df.columns) == ['timestamp', 'open', 'high', 'low', 'close', 'volume', 'symbol']
    assert std_df.iloc[0]['timestamp'] == pd.to_datetime('2022-01-03T09:00:00Z')
    assert std_df.iloc[0]['open'] == 100.0
    assert std_df.iloc[1]['close'] == 110.0
    assert std_df.iloc[1]['symbol'] == 'AAPL'


def test_standardize_bars_dataframe_missing_column(dummy_dao: DummyDAO) -> None:
    # Remove 't' column to simulate missing timestamp
    raw_df = pd.DataFrame(
        [
            {'o': 100.0, 'h': 110.0, 'l': 90.0, 'c': 105.0, 'v': 1000, 'symbol': 'AAPL'},
        ]
    )
    with pytest.raises(Exception):
        dummy_dao.standardize_bars_dataframe(raw_df, standard_mapping())


def test_standardize_bars_dataframe_invalid_timestamp(dummy_dao: DummyDAO) -> None:
    # Provide an invalid timestamp
    raw_df = pd.DataFrame(
        [
            {
                't': 'not-a-date',
                'o': 100.0,
                'h': 110.0,
                'l': 90.0,
                'c': 105.0,
                'v': 1000,
                'symbol': 'AAPL',
            },
        ]
    )
    # Should print a warning and raise on schema validation
    with pytest.raises(Exception):
        dummy_dao.standardize_bars_dataframe(raw_df, standard_mapping())
