from abc import ABC, abstractmethod

import pandas as pd
from pandera.typing.pandas import DataFrame

from trading_bot_mvp.service.base_service import BaseService, GeneratedAPIClient
from trading_bot_mvp.service.data.bars_column_models import (
    BarsColumnMapping,
    BarsSchema,
    StandardBarsColumns,
)
from trading_bot_mvp.shared.model import BarRequest


class BaseDAO(BaseService, ABC):
    """
    Abstract base DAO class for data access. Optionally takes a baseAPIclient for API interaction.
    """

    def __init__(self, api_client: GeneratedAPIClient | None = None) -> None:
        self.api_client = api_client

    @abstractmethod
    def get_bars(self, request: BarRequest) -> DataFrame[BarsSchema]:
        """
        Abstract method to fetch bars for a given symbol and timeframe.
        Should be implemented by subclasses.
        """
        pass

    def standardize_bars_dataframe(
        self, df: pd.DataFrame, column_mapping: BarsColumnMapping
    ) -> DataFrame[BarsSchema]:
        """
        Standardize a bars DataFrame to the expected column layout using a BarsColumnMapping.
        :param df: The input DataFrame with raw bars data.
        :param column_mapping: object mapping response column names to standard names.
        :return: DataFrame with standardized columns.
        """
        standardized_df = df.rename(columns=column_mapping.as_rename_dict())
        # Ensure is set to the timestamp column is datetime if it exists
        if StandardBarsColumns.timestamp in standardized_df.columns:
            try:
                standardized_df[StandardBarsColumns.timestamp] = pd.to_datetime(
                    standardized_df[StandardBarsColumns.timestamp], utc=True
                )
            except Exception:
                print(f'Failed to convert timestamp to datetime: {standardized_df.index}')
        return BarsSchema.validate(standardized_df)
