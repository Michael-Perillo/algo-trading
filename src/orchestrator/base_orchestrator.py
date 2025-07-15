from abc import ABC, abstractmethod
from typing import Any

from pydantic import BaseModel

from service.brokerage.base_brokerage_service import BaseBrokerageService
from service.data.base_dao import BaseDAO
from thesis.base_thesis import BaseThesis


class BaseOrchestrator(ABC, BaseModel):
    theses: list[BaseThesis]
    brokerage_service: BaseBrokerageService
    data_dao: BaseDAO

    model_config = {'arbitrary_types_allowed': True}

    @abstractmethod
    def run(self, *args: Any) -> None:
        """
        The main event loop of the trading bot.
        This method should be implemented by subclasses to define the orchestration logic.
        """
        pass
