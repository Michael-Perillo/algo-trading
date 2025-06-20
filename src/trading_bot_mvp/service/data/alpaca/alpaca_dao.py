import pandas as pd
from trading_bot_mvp.service.data.base_dao import BaseDAO
from trading_bot_mvp.service.brokerage.alpaca.alpaca_brokerage_service import AlpacaBrokerageService

from trading_bot_mvp.shared.model import BarRequest


class AlpacaDAO(BaseDAO):
    """
    Data Access Object for Alpaca brokerage, using AlpacaExecutionService for API operations.
    """
    service: AlpacaBrokerageService
    def __init__(self, service: AlpacaBrokerageService ):
        super().__init__(service)

    def get_bars(self, request: BarRequest) -> pd.DataFrame:
        """
        Fetch bars for a given symbol and timeframe using the Alpaca brokerage service.
        Note that this is somewhat of an anti-pattern, as the DAO is basically just wrapping the service.
        However, it allows for a consistent interface across different data sources should we need to support multiple data sources in the future.
        :param request: BarRequest containing symbol, timeframe, and other parameters.
        :return: DataFrame containing the requested bars.
        """

        # Convert response to DataFrame
        return self.service.get_bars(request)
