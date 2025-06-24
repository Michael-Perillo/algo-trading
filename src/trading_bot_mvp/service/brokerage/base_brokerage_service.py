from abc import ABC, abstractmethod

from trading_bot_mvp.service.base_service import BaseService, GeneratedAPIClient
from trading_bot_mvp.shared.model import Account, OrderRequest, OrderResponse, Position


class BaseBrokerageService(BaseService, ABC):
    """
    Abstract base brokerage service class for interacting with a brokerage.
    Optionally takes a baseAPIclient for API interaction.
    """

    def __init__(self, api_client: GeneratedAPIClient | None = None) -> None:
        self.api_client = api_client

    @abstractmethod
    def get_account(self) -> Account:
        """
        Abstract method to fetch account information using the shared model.
        Should be implemented by subclasses.
        """
        pass

    @abstractmethod
    def get_open_positions(self, symbol: str | None = None) -> list[Position]:
        """
        Abstract method to fetch open positions using the shared model.
        :param symbol: Optional symbol to filter positions by.
        Should be implemented by subclasses.
        """
        pass

    @abstractmethod
    def place_order(self, order_request: OrderRequest) -> OrderResponse:
        """
        Abstract method to place an order using the shared model.
        Should be implemented by subclasses.
        """
        pass
