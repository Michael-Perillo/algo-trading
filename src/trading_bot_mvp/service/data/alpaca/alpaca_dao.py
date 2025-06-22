import pandas as pd
from pandera.typing.pandas import DataFrame

from trading_bot_mvp.client.alpaca.alpaca_client import AlpacaDataClient
from trading_bot_mvp.client.alpaca.data_models import StockBarsResp
from trading_bot_mvp.client.base_client import BaseAPIClient
from trading_bot_mvp.service.data.bars_column_models import (
    BarsColumnMapping,
    BarsSchema,
    StandardBarsColumns,
)
from trading_bot_mvp.service.data.base_dao import BaseDAO
from trading_bot_mvp.shared.model import BarRequest


class AlpacaDAO(BaseDAO):
    """
    Data Access Object for Alpaca brokerage, using AlpacaExecutionService for API operations.
    """

    api_client: AlpacaDataClient

    def __init__(self, api_client: BaseAPIClient | None = None):
        if api_client is None:
            # Initialize the Alpaca API client if not provided
            api_client = AlpacaDataClient()
        super().__init__(api_client)

    def get_bars(self, request: BarRequest) -> DataFrame[BarsSchema]:
        """
        Fetch bars for a given symbol and timeframe using the Alpaca brokerage service.
        :param request: BarRequest containing parameters for fetching bars.
        :return: DataFrame with columns matching StandardBarsColumns
        (timestamp, open, high, low, close, volume, symbol, ...)
        """
        response = self.api_client.get_bars(
            request.symbol, request.timeframe.value, request.start, request.end
        )
        bars_response_body = StockBarsResp(**response.json())
        bars_dict = bars_response_body.bars
        all_bars = []
        for symbol, bars in bars_dict.items():
            for bar in bars:
                bar_dict = dict(bar)
                ts = getattr(bar_dict.get('t'), 'root', None)
                if ts is None:
                    ts = bar_dict.get('t')
                if ts is None:
                    raise ValueError('Bar timestamp is None and cannot be converted to datetime.')
                # Ensure ts is str or datetime for pandas
                if not isinstance(ts, str | pd.Timestamp):
                    ts = str(ts)
                pd_ts = (
                    pd.to_datetime(ts).tz_convert('UTC')
                    if pd.to_datetime(ts).tzinfo
                    else pd.to_datetime(ts).tz_localize('UTC')
                )
                bar_dict['t'] = pd_ts
                bar_dict['symbol'] = symbol
                all_bars.append(bar_dict)
        df = pd.DataFrame(all_bars)
        # Use the standardize_bars_dataframe method to return the standard layout
        standard_mapping = BarsColumnMapping(
            mapping={
                't': StandardBarsColumns().timestamp,
                'o': StandardBarsColumns().open,
                'h': StandardBarsColumns().high,
                'l': StandardBarsColumns().low,
                'c': StandardBarsColumns().close,
                'v': StandardBarsColumns().volume,
                'symbol': StandardBarsColumns().symbol,
            }
        )
        return self.standardize_bars_dataframe(df, standard_mapping)
