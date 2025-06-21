import pandas as pd

from trading_bot_mvp.client.alpaca.alpaca_client import AlpacaDataClient
from trading_bot_mvp.client.alpaca.data_models import StockBarsResp
from trading_bot_mvp.service.data.base_dao import BaseDAO
from trading_bot_mvp.service.data.bars_column_models import BarsColumnMapping, StandardBarsColumns, BarsSchema
from trading_bot_mvp.shared.model import BarRequest
from pandera.typing.pandas import DataFrame




class AlpacaDAO(BaseDAO):
    """
    Data Access Object for Alpaca brokerage, using AlpacaExecutionService for API operations.
    """
    api_client: AlpacaDataClient
    def __init__(self, api_client: AlpacaDataClient = None):
        if api_client is None:
            # Initialize the Alpaca API client if not provided
            api_client = AlpacaDataClient()
        super().__init__(api_client)

    def get_bars(self, request: BarRequest) -> DataFrame[BarsSchema]:
        """
        Fetch bars for a given symbol and timeframe using the Alpaca brokerage service.
        :param request: BarRequest containing parameters for fetching bars.
        :return: DataFrame with columns matching StandardBarsColumns (timestamp, open, high, low, close, volume, symbol, ...)
        """
        response = self.api_client.get_bars(request.symbol, request.timeframe.value, request.start, request.end)
        bars_response_body = StockBarsResp(**response.json())
        bars_dict = bars_response_body.bars
        if isinstance(bars_dict, dict):
            all_bars = []
            for symbol, bars in bars_dict.items():
                for bar in bars:
                    bar = dict(bar)  # ensure mutable
                    bar['symbol'] = symbol
                    all_bars.append(bar)
            df = pd.DataFrame(all_bars)
        else:
            # fallback for flat list
            df = pd.DataFrame(bars_dict)
            df['symbol'] = request.symbol
        # set the index to the timestamp if present
        if 't' in df.columns:
            df.set_index('t', inplace=True)
            try:
                df.index = pd.to_datetime(df.index)
            except Exception:
                pass
        # Use the standardize_bars_dataframe method to return the standard layout
        standard_mapping = BarsColumnMapping(mapping={
            't': StandardBarsColumns().timestamp,
            'o': StandardBarsColumns().open,
            'h': StandardBarsColumns().high,
            'l': StandardBarsColumns().low,
            'c': StandardBarsColumns().close,
            'v': StandardBarsColumns().volume,
            'symbol': StandardBarsColumns().symbol,
        })
        return self.standardize_bars_dataframe(df, standard_mapping)
