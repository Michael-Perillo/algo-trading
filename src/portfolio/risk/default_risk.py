from portfolio.risk.base_risk import BaseRisk


class DefaultRisk(BaseRisk):
    """
    Default risk management strategy.
    Implements basic risk management parameters.
    """

    stop_loss_percentage: float = 0.02  # 2% stop loss
    take_profit_percentage: float = 0.06  # 6% take profit
