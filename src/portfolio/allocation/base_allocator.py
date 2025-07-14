from abc import ABC, abstractmethod

from portfolio.risk.base_risk import BaseRisk
from shared.model import Account, Allocation, Position


class BaseAllocator(ABC):
    @abstractmethod
    def allocate(
        self,
        account: Account,
        latest_price: float,
        risk_management: BaseRisk,
        current_position: Position | None = None,
    ) -> Allocation:
        """
        Calculate the position size (quantity) for a given asset.
        Returns the quantity to order.
        """
        pass
