from abc import ABC, abstractmethod
from typing import Optional
import pandas as pd

from trading_bot_mvp.service.base_service import BaseService
from trading_bot_mvp.shared.model import BarRequest


class BaseDAO(ABC):
    """
    Abstract base DAO class for data access. Optionally takes a BaseService for API/service interaction.
    """
    def __init__(self, service: Optional[BaseService] = None):
        self.service = service

    @abstractmethod
    def get_bars(self, request: BarRequest) -> pd.DataFrame:
        """
        Abstract method to fetch bars for a given symbol and timeframe.
        Should be implemented by subclasses.
        """
        pass
