from abc import ABC
from trading_bot_mvp.client.base_client import BaseAPIClient
from typing import Type, Dict, Any, TypeVar
from pydantic import BaseModel

from trading_bot_mvp.shared.model import FieldMap

GenericBaseModel = TypeVar('GenericBaseModel', bound=BaseModel)


class BaseService(ABC):
    """
    Base service class that uses an API client to interact with an external API.
    Subclasses should implement domain-specific logic and response parsing.
    """
    def __init__(self, api_client: BaseAPIClient):
        self.api_client = api_client

    @staticmethod
    def map_model(source: BaseModel, target_model: Type[GenericBaseModel], field_map: FieldMap = None) -> GenericBaseModel:
        """
        Map fields from a source Pydantic model to a target Pydantic model, optionally renaming fields using a FieldMap.
        Main use case is to convert between different API response models or DTOs (Data Transfer Objects).
        :param source: The source Pydantic model instance
        :param target_model: The target Pydantic model class
        :param field_map: Optional FieldMap instance for mapping source to target fields
        :return: An instance of the target_model
        """
        data = source.model_dump()
        if field_map:
            mapped_data = {k: data.get(v, None) for k, v in field_map.mapping.items()}
        else:
            mapped_data = data
        return target_model.model_validate(mapped_data)
