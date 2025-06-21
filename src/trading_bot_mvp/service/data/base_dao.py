from typing import Optional
from abc import ABC, abstractmethod
import pandas as pd

from trading_bot_mvp.client.base_client import BaseAPIClient
from trading_bot_mvp.service.base_service import BaseService
from trading_bot_mvp.shared.model import BarRequest
from trading_bot_mvp.service.data.bars_column_models import BarsColumnMapping, BarsSchema
from pandera.typing.pandas import DataFrame


class BaseDAO(BaseService, ABC):
    """
    Abstract base DAO class for data access. Optionally takes a baseAPIclient for API interaction.
    """
    def __init__(self, api_client: Optional[BaseAPIClient] = None) -> None:
        self.api_client = api_client

    @abstractmethod
    def get_bars(self, request: BarRequest) -> DataFrame[BarsSchema]:
        """
        Abstract method to fetch bars for a given symbol and timeframe.
        Should be implemented by subclasses.
        """
        pass

    def standardize_bars_dataframe(self, df: pd.DataFrame, column_mapping: BarsColumnMapping) -> DataFrame[BarsSchema]:
        """
        Standardize a bars DataFrame to the expected column layout using a BarsColumnMapping.
        :param df: The input DataFrame with raw bars data.
        :param column_mapping: BarsColumnMapping object mapping standard column names to response column names.
        :return: DataFrame with standardized columns.
        """
        standardized_df = df.rename(columns=column_mapping.mapping)
        return standardized_df
