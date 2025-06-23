import pandas as pd
from pandera.typing.pandas import DataFrame

from trading_bot_mvp.client.alpaca.adapters import alpaca_bars_column_mapping as standard_mapping
from trading_bot_mvp.service.data.bars_column_models import BarsSchema
from trading_bot_mvp.service.data.base_dao import BaseDAO
from trading_bot_mvp.shared.mocks import mocks
from trading_bot_mvp.shared.mocks.mocks import DummyAPIClient
from trading_bot_mvp.shared.model import BarRequest, Timeframe


class DummyDAO(BaseDAO):
    def __init__(self, api_client: DummyAPIClient = mocks.DummyAPIClient()):
        super().__init__(api_client)

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


bar_request = BarRequest(symbol='AAPL', timeframe=Timeframe.field_1D, start=None, end=None)


def test_standardize_bars_dataframe() -> None:
    # Define a mapping from standard to desired output columns (e.g., 'timestamp', 'open', ...)
    dao = DummyDAO()
    std_df = dao.get_bars(bar_request)
    # Assert columns are renamed to the new standard
    assert list(std_df.columns) == [
        'timestamp',
        'open',
        'high',
        'low',
        'close',
        'volume',
        'symbol',
    ]
    # Assert data is preserved
    # check the index
    assert std_df.iloc[0]['timestamp'] == pd.to_datetime('2022-01-03T09:00:00Z')
    assert std_df.iloc[0]['open'] == 100.0
    assert std_df.iloc[1]['close'] == 110.0
    assert std_df.iloc[1]['symbol'] == 'AAPL'
