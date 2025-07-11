from pydantic import BaseModel

from service.brokerage.base_brokerage_service import BaseBrokerageService
from service.data.base_dao import BaseDAO
from shared.model import (
    BarRequest,
    OrderClass,
    OrderRequest,
    OrderSide,
    OrderType,
    Timeframe,
    TimeInForce,
)
from strategy.base_strategy import BaseStrategy, Signal


class RiskManagement(BaseModel):
    risk_per_trade_percentage: float = 0.01
    stop_loss_percentage: float = 0.02
    take_profit_percentage: float = 0.04


class TradingThesis(BaseModel):
    thesis_name: str
    asset_universe: list[str]
    strategy: BaseStrategy
    risk_management: RiskManagement
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
            bars_request = BarRequest(
                symbol=asset,
                timeframe=Timeframe.field_1D,  # Daily bars
                start=None,  # Use default start time
                end=None,  # Use default end time
            )
            bars_df = self.data_dao.get_bars(bars_request)
            if bars_df.empty:
                print(f'No data for {asset}, skipping.')
                continue

            latest_signal = self.strategy.generate_signal(bars_df)
            latest_price = bars_df['close'].iloc[-1]
            current_position = positions.get(asset)

            # --- Position Sizing Logic ---
            # todo: Implement position sizing taking into account: allocation, volatility, etc.
            # todo: Position sizing services should be injected into the thesis
            if latest_signal == Signal.BUY and not current_position:
                trade_risk_capital = (
                    float(account_info.cash) * self.risk_management.risk_per_trade_percentage
                )
                stop_loss_price = latest_price * (1 - self.risk_management.stop_loss_percentage)
                risk_per_share = latest_price - stop_loss_price
                #
                # if risk_per_share <= 0:
                #     continue
                #
                qty = trade_risk_capital // risk_per_share
                #
                # if qty == 0:
                #     print(f'[{self.thesis_name}] Not enough capital to place trade for {asset}.')
                #     continue

                orders.append(
                    OrderRequest(
                        symbol=asset,
                        qty=qty,
                        side=OrderSide.buy,
                        type=OrderType.market,
                        time_in_force=TimeInForce.gtc,
                        order_class=OrderClass.bracket,
                        stop_loss_price=round(stop_loss_price, 2),
                        take_profit_price=round(
                            latest_price * (1 + self.risk_management.take_profit_percentage), 2
                        ),
                        limit_price=None,
                        stop_price=None,
                        client_order_id=None,
                        metadata=None,
                    )
                )

            elif latest_signal == Signal.SELL and current_position:
                orders.append(
                    OrderRequest(
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
                )

        return orders
