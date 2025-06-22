from abc import ABC, abstractmethod

from trading_bot_mvp.client.base_client import BaseAPIClient
from trading_bot_mvp.service.base_service import BaseService
from trading_bot_mvp.shared.model import Account


class BaseBrokerageService(BaseService, ABC):
    """
    Abstract base brokerage service class for interacting with a brokerage.
    Optionally takes a baseAPIclient for API interaction.
    """

    def __init__(self, api_client: BaseAPIClient | None = None) -> None:
        self.api_client = api_client

    @abstractmethod
    def get_account(self) -> Account:
        """
        Abstract method to fetch account information using the shared model.
        Should be implemented by subclasses.
        """
        pass
