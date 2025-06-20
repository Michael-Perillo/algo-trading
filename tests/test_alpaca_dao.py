import pandas as pd
import pytest
from trading_bot_mvp.service.data.alpaca.alpaca_dao import AlpacaDAO
from trading_bot_mvp.shared.model import BarRequest

class DummyBrokerageService:
    def get_bars(self, request):
        # Return a DataFrame as expected by the DAO
        return pd.DataFrame([
            {"id": "1", "symbol": "AAPL", "status": "filled"},
            {"id": "2", "symbol": "TSLA", "status": "new"}
        ])

@pytest.fixture
def alpaca_dao():
    service = DummyBrokerageService()
    return AlpacaDAO(service)

def test_get_bars(alpaca_dao):
    request = BarRequest(symbol="AAPL", timeframe="1d")
    df = alpaca_dao.get_bars(request)
    assert isinstance(df, pd.DataFrame)
    assert "id" in df.columns
    assert df.iloc[0]["id"] == "1"
    assert df.iloc[0]["symbol"] == "AAPL"
    assert df.iloc[0]["status"] == "filled"
    assert df.iloc[1]["id"] == "2"
    assert df.iloc[1]["symbol"] == "TSLA"
    assert df.iloc[1]["status"] == "new"
