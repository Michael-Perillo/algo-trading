import pandas as pd
from trading_bot_mvp.client.alpaca.data_models import BarsResponse
from trading_bot_mvp.service.base_service import BaseService
from trading_bot_mvp.client.alpaca.alpaca_client import AlpacaAPIClient
from trading_bot_mvp.client.alpaca.trading_models import Account as AlpacaAccountResponseBody
from trading_bot_mvp.shared.model import Account
from trading_bot_mvp.shared.model import BarRequest
import trading_bot_mvp.service.brokerage.alpaca.api_field_mappings.model as alpaca_field_mappings


class AlpacaBrokerageService(BaseService):
    api_client: AlpacaAPIClient

    def __init__(self, api_client: AlpacaAPIClient):
        super().__init__(api_client)

    def get_account(self) -> Account:
        response = self.api_client.get_account()
        account_response_body = AlpacaAccountResponseBody(**response.json())
        return self.map_model(account_response_body, Account, alpaca_field_mappings.AccountFieldMap())

    def get_bars(self, request: BarRequest) -> pd.DataFrame:
        """
        Fetch bars for a given symbol and timeframe using the Alpaca brokerage service.
        :param request: APIRequest containing parameters for fetching bars.
        :return: List of bar data as dictionaries.
        """
        # todo need a common interface for bar response tables
        # dereference the bar request to get the parameters
        response = self.api_client.get_bars(request.symbol, request.start, request.end, request.timeframe.value)
        bars_response_body = BarsResponse(**response.json())
        # Convert the response to a DataFrame
        df = pd.DataFrame(bars_response_body.bars)
        # add the symbol column
        df['symbol'] = request.symbol
        # set the index to the timestamp
        df.set_index('timestamp', inplace=True)
        # convert the timestamp to datetime
        df.index = pd.to_datetime(df.index, unit='s')
        # check if the paging key is present in the response
        if bars_response_body.next_page_token:
            # if it is, we need to loop through the pages until we have all the data
            while bars_response_body.next_page_token:
                response = self.api_client.get_bars(request.symbol, request.start, request.end, request.timeframe.value, page_token=bars_response_body.next_page_token)
                bars_response_body = BarsResponse(**response.json())
                # Convert the response to a DataFrame
                df_next = pd.DataFrame(bars_response_body.bars)
                # add the symbol column
                df_next['symbol'] = request.symbol
                # set the index to the timestamp
                df_next.set_index('timestamp', inplace=True)
                # convert the timestamp to datetime
                df_next.index = pd.to_datetime(df_next.index, unit='s')
                # append the new data to the existing DataFrame
                df = pd.concat([df, df_next])
        return df
