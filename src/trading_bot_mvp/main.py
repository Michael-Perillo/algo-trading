from datetime import date

from trading_bot_mvp.service.brokerage.alpaca.alpaca_brokerage_service import (
    AlpacaBrokerageService,
)
from trading_bot_mvp.service.data.alpaca.alpaca_dao import AlpacaDAO
from trading_bot_mvp.shared.model import BarRequest, Timeframe

if __name__ == '__main__':
    # Initialize the Alpaca API client and services
    brokerage_service = AlpacaBrokerageService()
    alpaca_dao = AlpacaDAO()

    # Get account info
    print('--- Account Info ---')
    account = brokerage_service.get_account()
    print(account)

    # Get bars for a symbol
    print('\n--- Bars Data ---')
    bar_request = BarRequest(
        symbol='AAPL',
        timeframe=Timeframe.field_1D,
        start=date(2023, 1, 1),
        end=date(2023, 2, 1),
    )
    bars_df = alpaca_dao.get_bars(bar_request)
    print(bars_df.head())

    # Optionally, use the DAO to get orders (example)
    # print("\n--- Orders ---")
    # orders = alpaca_dao.list()
    # print(orders)
