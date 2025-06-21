import pandas as pd
import pytest
from trading_bot_mvp.service.data.base_dao import BaseDAO
from trading_bot_mvp.service.data.bars_column_models import BarsColumnMapping
from trading_bot_mvp.service.data.bars_column_models import StandardBarsColumns

class DummyDAO(BaseDAO):
    def get_bars(self, request):
        pass

    def standardize_bars_dataframe(self, raw_df, mapping):
        # Renaming logic based on the provided mapping
        return raw_df.rename(columns=mapping.mapping)

def test_standardize_bars_dataframe():
    # Simulate a raw bars DataFrame with standard column names (e.g., 't', 'o', ...)
    raw_df = pd.DataFrame([
        {"t": "2022-01-03T09:00:00Z", "o": 100, "h": 110, "l": 90, "c": 105, "v": 1000, "symbol": "AAPL"},
        {"t": "2022-01-04T09:00:00Z", "o": 105, "h": 115, "l": 95, "c": 110, "v": 1200, "symbol": "AAPL"}
    ])
    # Define a mapping from standard to desired output columns (e.g., 'timestamp', 'open', ...)
    standard_mapping = BarsColumnMapping(mapping={
        't': StandardBarsColumns().timestamp,
        'o': StandardBarsColumns().open,
        'h': StandardBarsColumns().high,
        'l': StandardBarsColumns().low,
        'c': StandardBarsColumns().close,
        'v': StandardBarsColumns().volume,
        'symbol': StandardBarsColumns().symbol,
    })
    dao = DummyDAO()
    std_df = dao.standardize_bars_dataframe(raw_df, standard_mapping)
    # Assert columns are renamed to the new standard
    assert list(std_df.columns) == ["timestamp", "open", "high", "low", "close", "volume", "symbol"]
    # Assert data is preserved
    assert std_df.iloc[0]["timestamp"] == "2022-01-03T09:00:00Z"
    assert std_df.iloc[0]["open"] == 100
    assert std_df.iloc[1]["close"] == 110
    assert std_df.iloc[1]["symbol"] == "AAPL"
