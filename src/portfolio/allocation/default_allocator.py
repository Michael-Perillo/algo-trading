from shared.model import Account, Allocation, Position

from ..risk.base_risk import BaseRisk
from .base_allocator import BaseAllocator


class DefaultAllocator(BaseAllocator):
    def allocate(
        self,
        account: Account,
        latest_price: float,
        risk_management: BaseRisk,
        current_position: Position | None = None,
    ) -> Allocation:
        """
        Basic allocation logic: risk per trade, stop loss, and volatility.
        Returns the quantity to order.
        """
        stop_loss_price = risk_management.calculate_stop_loss(latest_price)
        take_profit_price = risk_management.calculate_take_profit(latest_price)
        trade_risk_capital = risk_management.calculate_trade_risk_capital(account.cash)
        qty = int(trade_risk_capital / latest_price)
        return Allocation(
            quantity=qty,
            entry_price=latest_price,
            stop_loss_price=stop_loss_price,
            take_profit_price=take_profit_price,
            metadata=None,
        )
