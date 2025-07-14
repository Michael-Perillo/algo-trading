from abc import ABC, abstractmethod
from datetime import datetime

from pydantic import BaseModel

from portfolio.allocation.base_allocator import BaseAllocator
from portfolio.risk.base_risk import BaseRisk
from service.brokerage.base_brokerage_service import BaseBrokerageService
from service.data.base_dao import BaseDAO
from shared.model import OrderRequest
from strategy.base_strategy import BaseStrategy


class BaseThesis(BaseModel, ABC):
    """
    An abstract base class for a trading thesis.
    A thesis uses strategies, data, and allocators to generate orders.
    """

    thesis_name: str
    asset_universe: list[str]
    strategy: BaseStrategy
    risk_management: BaseRisk
    data_dao: BaseDAO  # Injected DAO for data access
    brokerage_service: BaseBrokerageService  # Injected brokerage service for account/positions
    allocator: BaseAllocator
    start_timestamp: datetime

    model_config = {'arbitrary_types_allowed': True}

    @abstractmethod
    def generate_order(self) -> list[OrderRequest]:
        """
        Abstract method to generate a list of OrderRequest objects.
        Must be implemented by subclasses.
        """
        pass
