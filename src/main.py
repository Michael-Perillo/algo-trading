import datetime as dt
import logging

from orchestrator.default_orchestrator import DefaultOrchestrator
from service.brokerage.alpaca.alpaca_brokerage_service import (
    AlpacaBrokerageService,
)
from service.data.alpaca.alpaca_dao import AlpacaDAO
from shared.model import BarRequest, Timeframe
from thesis.SMA_thesis import SMACrossoverThesis

# Set up logging for the entire application
logging.basicConfig(
    level=logging.INFO,  # Set to DEBUG for verbose output
    format='%(asctime)s %(levelname)s %(name)s: %(message)s',
)

# Initialize the Alpaca API client and services
brokerage_service = AlpacaBrokerageService()
alpaca_dao = AlpacaDAO()


def run_orchestrator() -> None:
    # Initialize the trading thesis
    thesis = SMACrossoverThesis(
        data_dao=alpaca_dao,
        brokerage_service=brokerage_service,
        start_timestamp=dt.datetime.now(dt.UTC),  # Use current time
    )

    # Create the orchestrator
    orchestrator = DefaultOrchestrator(
        theses=[thesis],
        brokerage_service=brokerage_service,
        data_dao=alpaca_dao,
    )

    # Run the orchestrator
    orchestrator.run(interval_seconds=60)


if __name__ == '__main__':
    # Get account info
    print('--- Account Info ---')
    account = brokerage_service.get_account()
    print(account)

    # Get bars for a symbol
    print('\n--- Bars Data ---')
    bar_request = BarRequest(
        symbol='AAPL',
        timeframe=Timeframe.field_1m,
        start=dt.date(2023, 1, 1),
        end=dt.date(2023, 2, 1),
    )
    bars_df = alpaca_dao.get_bars(bar_request)
    print(bars_df.head())

    # Run the orchestrator with the trading thesis
    run_orchestrator()
