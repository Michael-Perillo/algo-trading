from datetime import date

from pandera.typing.pandas import DataFrame

from portfolio.allocation.base_allocator import BaseAllocator
from portfolio.allocation.default_allocator import DefaultAllocator
from portfolio.risk.base_risk import BaseRisk
from portfolio.risk.default_risk import DefaultRisk
from service.brokerage.base_brokerage_service import BaseBrokerageService
from service.data.bars_column_models import BarsSchema
from service.data.base_dao import BaseDAO
from shared.model import (
    Account,
    BarRequest,
    OrderClass,
    OrderRequest,
    OrderSide,
    OrderType,
    Position,
    Timeframe,
    TimeInForce,
)
from strategy.base_strategy import BaseStrategy, Signal
from strategy.moving_average_crossover import MovingAverageCrossover
from thesis.base_thesis import BaseThesis


class SMACrossoverThesis(BaseThesis):
    thesis_name: str = 'SMA Crossover Thesis'
    asset_universe: list[str] = ['AAPL', 'MSFT', 'GOOGL']  # Example asset universe
    strategy: BaseStrategy = MovingAverageCrossover(short_window=20, long_window=50)
    risk_management: BaseRisk = DefaultRisk()
    allocator: BaseAllocator = DefaultAllocator()
    data_dao: BaseDAO  # Injected DAO for data access
    brokerage_service: BaseBrokerageService  # Injected brokerage service for account/positions

    model_config = {'arbitrary_types_allowed': True}

    def generate_order(self) -> list[OrderRequest]:
        """
        For each asset in the universe, fetch data, generate signals, and decide on orders.
        Returns a list of OrderRequest objects to be placed.
        """
        account_info = self.brokerage_service.get_account()
        positions = {p.symbol: p for p in self.brokerage_service.get_open_positions()}
        orders = []

        for asset in self.asset_universe:
            order_request = self.generate_and_interpret_signal(
                asset, positions.get(asset), account_info
            )
            if order_request:
                orders.append(order_request)
        return orders

    def generate_and_interpret_signal(
        self, asset: str, current_position: Position | None, account: Account
    ) -> OrderRequest | None:
        # todo: need to fetch bars since starting date, not just the latest or save them as we go
        bars_df = self.fetch_bars(asset)
        if bars_df is None or bars_df.empty:
            print(f'No bars data for {asset}, skipping.')
            return None
        latest_signal = self.strategy.generate_signal(bars=bars_df)
        if latest_signal == Signal.BUY and not current_position:
            allocation = self.allocator.allocate(
                account=account,
                latest_price=bars_df.iloc[-1].price,
                risk_management=self.risk_management,
            )
            stop_loss_price = None
            take_profit_price = None
            if allocation.stop_loss_price:  # Ensure stop loss is set
                stop_loss_price = round(allocation.stop_loss_price, 2)
            if allocation.take_profit_price:
                take_profit_price = round(allocation.take_profit_price, 2)
            return OrderRequest(
                symbol=asset,
                qty=allocation.quantity,
                side=OrderSide.buy,
                type=OrderType.market,
                time_in_force=TimeInForce.gtc,
                order_class=OrderClass.bracket,
                stop_loss_price=stop_loss_price,
                take_profit_price=take_profit_price,
                limit_price=None,
                stop_price=None,
                client_order_id=None,
                metadata=None,
            )
        elif latest_signal == Signal.SELL and current_position:
            return OrderRequest(
                symbol=asset,
                qty=current_position.qty,
                side=OrderSide.sell,
                type=OrderType.market,
                time_in_force=TimeInForce.gtc,
                limit_price=None,
                stop_price=None,
                take_profit_price=None,
                stop_loss_price=None,
                order_class=OrderClass.simple,
                client_order_id=None,
                metadata=None,
            )
        elif latest_signal == Signal.HOLD:
            return None
        return None

    def fetch_bars(
        self, asset: str, start: date | None = None, end: date | None = None
    ) -> DataFrame[BarsSchema] | None:
        bars_request = BarRequest(
            symbol=asset,
            timeframe=Timeframe.field_1D,  # Daily bars
            start=start,  # Use default start time
            end=end,  # Use default end time
        )
        bars_df = self.data_dao.get_bars(bars_request)
        if bars_df.empty:
            print(f'No data for {asset}, skipping.')
            return None
        return bars_df
