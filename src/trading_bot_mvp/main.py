import pandas as pd

from trading_bot_mvp.client.alpaca.alpaca_client import AlpacaAPIClient
from trading_bot_mvp.service.brokerage.alpaca.alpaca_brokerage_service import AlpacaBrokerageService
from trading_bot_mvp.service.data.alpaca.alpaca_dao import AlpacaDAO
from trading_bot_mvp.shared.model import BarRequest

if __name__ == "__main__":
    # Initialize the Alpaca API client and services
    api_client = AlpacaAPIClient()
    brokerage_service = AlpacaBrokerageService(api_client)
    alpaca_dao = AlpacaDAO(brokerage_service)

    # Get account info
    print("--- Account Info ---")
    account = brokerage_service.get_account()
    print(account)

    # Get bars for a symbol
    print("\n--- Bars Data ---")
    # todo fix the request issue with start and end dates
    bar_request = BarRequest(symbol="AAPL", timeframe="1d", start=pd.to_datetime("2023-01-01"), end=pd.to_datetime("2023-02-01"))
    bars_df = alpaca_dao.get_bars(bar_request)
    print(bars_df.head())

    # Optionally, use the DAO to get orders (example)
    # print("\n--- Orders ---")
    # orders = alpaca_dao.list()
    # print(orders)

