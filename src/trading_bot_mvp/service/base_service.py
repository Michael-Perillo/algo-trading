from abc import ABC
from typing import TypeVar

from pydantic import BaseModel

from trading_bot_mvp.client.base_client import BaseAPIClient

GenericBaseModel = TypeVar('GenericBaseModel', bound=BaseModel)


class BaseService(ABC):
    """
    Base service class that uses an API client to interact with an external API.
    Subclasses should implement domain-specific logic and response parsing.
    """

    def __init__(self, api_client: BaseAPIClient | None = None):
        self.api_client = api_client
