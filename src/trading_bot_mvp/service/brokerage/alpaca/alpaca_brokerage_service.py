import pandas as pd
from trading_bot_mvp.client.alpaca.data_models import StockBarsResp
from trading_bot_mvp.service.base_service import BaseService
from trading_bot_mvp.client.alpaca.alpaca_client import AlpacaAPIClient, AlpacaDataClient
from trading_bot_mvp.client.alpaca.trading_models import Account as AlpacaAccountResponseBody
from trading_bot_mvp.shared.model import Account
from trading_bot_mvp.shared.model import BarRequest
import trading_bot_mvp.service.brokerage.alpaca.api_field_mappings.model as alpaca_field_mappings


class AlpacaBrokerageService(BaseService):
    api_client: AlpacaAPIClient
    data_client: AlpacaDataClient

    def __init__(self, api_client: AlpacaAPIClient):
        super().__init__(api_client)
        self.data_client = AlpacaDataClient()

    def get_account(self) -> Account:
        response = self.api_client.get_account()
        account_response_body = AlpacaAccountResponseBody(**response.json())
        return self.map_model(account_response_body, Account, alpaca_field_mappings.AccountFieldMap())

    def get_bars(self, request: BarRequest) -> pd.DataFrame:
        """
        Fetch bars for a given symbol and timeframe using the Alpaca brokerage service.
        :param request: BarRequest containing parameters for fetching bars.
        :return: DataFrame of bar data with symbol column.
        """
        response = self.data_client.get_bars(request.symbol, request.start, request.end, request.timeframe.value)
        bars_response_body = StockBarsResp(**response.json())
        # Handle non-flat bars response: bars is a dict keyed by symbol
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
        return df
