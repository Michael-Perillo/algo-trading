from typing import Dict
from pydantic import BaseModel, Field
import pandera.pandas as pa

class StandardBarsColumns(BaseModel):
    timestamp: str = Field(default="timestamp", description="Timestamp column name")
    open: str = Field(default="open", description="Open price column name")
    high: str = Field(default="high", description="High price column name")
    low: str = Field(default="low", description="Low price column name")
    close: str = Field(default="close", description="Close price column name")
    volume: str = Field(default="volume", description="Volume column name")
    symbol: str = Field(default="symbol", description="Symbol column name")
    # Add more standard columns as needed

cols = StandardBarsColumns()

class BarsSchema(pa.DataFrameModel):
    __annotations__ = {
        cols.timestamp: pa.typing.Index[pa.Timestamp],
        cols.open: float,
        cols.high: float,
        cols.low: float,
        cols.close: float,
        cols.volume: int,
        cols.symbol: str,
    }

class BarsColumnMapping(BaseModel):
    mapping: Dict[str, str] = Field(..., description="Mapping from standard column names to response column names")

