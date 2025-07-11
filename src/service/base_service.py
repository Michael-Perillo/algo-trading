from abc import ABC
from typing import Protocol


class GeneratedAPIClient(Protocol):
    # Mainly for type hinting
    pass


class BaseService(ABC):
    """
    Base service class that uses an API client to interact with an external API.
    Subclasses should implement domain-specific logic and response parsing.
    """

    def __init__(self, api_client: GeneratedAPIClient | None = None):
        self.api_client = api_client
