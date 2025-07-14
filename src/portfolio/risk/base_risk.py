from abc import ABC

from pydantic import BaseModel


class BaseRisk(BaseModel, ABC):
    stop_loss_percentage: float
    take_profit_percentage: float
    risk_per_trade_percentage: float = 0.005  # .5% of account equity per trade

    def calculate_stop_loss(self, entry_price: float) -> float:
        """
        Calculate the stop loss price based on the entry price and stop loss percentage.
        """
        return entry_price * (1 - self.stop_loss_percentage)

    def calculate_take_profit(self, entry_price: float) -> float:
        """
        Calculate the take profit price based on the entry price and take profit percentage.
        """
        return entry_price * (1 + self.take_profit_percentage)

    def calculate_trade_risk_capital(self, account_equity: float) -> float:
        """
        Calculate the capital allocated to a trade based on the account equity and percentage.
        """
        return account_equity * self.risk_per_trade_percentage
