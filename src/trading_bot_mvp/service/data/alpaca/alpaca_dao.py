from typing import Any

import pandas as pd
from pandera.typing.pandas import DataFrame

from trading_bot_mvp.client.alpaca.adapters import alpaca_bars_column_mapping
from trading_bot_mvp.client.alpaca.generated.alpaca_data.api.stock.stock_bars import (
    sync as get_stock_bars,
)
from trading_bot_mvp.client.alpaca.generated.alpaca_data.client import (
    Client as AlpacaDataClient,
)
from trading_bot_mvp.client.alpaca.generated.alpaca_data.models.stock_bars_resp import (
    StockBarsResp,
)
from trading_bot_mvp.client.alpaca.generated.alpaca_data.types import UNSET
from trading_bot_mvp.client.client_factory import get_alpaca_data_client
from trading_bot_mvp.service.data.bars_column_models import BarsSchema
from trading_bot_mvp.service.data.base_dao import BaseDAO
from trading_bot_mvp.shared.model import BarRequest


class AlpacaDAO(BaseDAO):
    """
    Data Access Object for Alpaca brokerage, using AlpacaExecutionService for API operations.
    """

    def __init__(self, api_client: AlpacaDataClient | None = None):
        self.api_client: AlpacaDataClient
        if api_client is None:
            # Initialize the Alpaca API client if not provided
            api_client = get_alpaca_data_client()
        super().__init__(api_client)

    def get_bars(self, request: BarRequest) -> DataFrame[BarsSchema]:
        """
        Fetch bars for a given symbol and timeframe using the Alpaca brokerage service.
        :param request: BarRequest containing parameters for fetching bars.
        :return: DataFrame with columns matching StandardBarsColumns
        (timestamp, open, high, low, close, volume, symbol, ...)
        """

        bars_response_body = get_stock_bars(
            client=self.api_client,
            symbols=request.symbol,
            timeframe=request.timeframe.value,
            start=request.start if request.start is not None else UNSET,
            end=request.end if request.end is not None else UNSET,
        )
        if bars_response_body is None:
            raise ValueError('Failed to fetch bars from Alpaca. Response body is None.')

        return self.standardize_bars_dataframe(
            self.parse_bars_response(bars_response_body), alpaca_bars_column_mapping()
        )

    def parse_bars_response(self, bars_response_body: StockBarsResp) -> DataFrame[Any]:
        bars_dict = bars_response_body.bars.to_dict()
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
        return DataFrame(pd.DataFrame(all_bars))
