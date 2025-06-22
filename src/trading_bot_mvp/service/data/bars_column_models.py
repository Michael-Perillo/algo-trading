import pandas as pd
import pandera.pandas as pa
from pydantic import BaseModel, Field


class StandardBarsColumns(BaseModel):
    timestamp: str = Field(default='timestamp', description='Timestamp column name')
    open: str = Field(default='open', description='Open price column name')
    high: str = Field(default='high', description='High price column name')
    low: str = Field(default='low', description='Low price column name')
    close: str = Field(default='close', description='Close price column name')
    volume: str = Field(default='volume', description='Volume column name')
    symbol: str = Field(default='symbol', description='Symbol column name')
    # Add more standard columns as needed


StandardColumns = StandardBarsColumns()

# get the type of index_datatype


class BarsSchema(pa.DataFrameModel):
    __annotations__ = {
        StandardColumns.timestamp: pd.DatetimeTZDtype('ns', 'UTC'),
        StandardColumns.open: float,
        StandardColumns.high: float,
        StandardColumns.low: float,
        StandardColumns.close: float,
        StandardColumns.volume: int,
        StandardColumns.symbol: str,
    }


class BarsColumnMapping(BaseModel):
    mapping: dict[str, str] = Field(
        ..., description='Mapping from standard column names to response column names'
    )
