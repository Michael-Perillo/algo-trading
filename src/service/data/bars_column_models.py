from enum import Enum

import pandas as pd
import pandera.pandas as pa
from pydantic import BaseModel


class StandardBarsColumns(str, Enum):
    timestamp = 'timestamp'
    open = 'open'
    high = 'high'
    low = 'low'
    close = 'close'
    volume = 'volume'
    symbol = 'symbol'


class BarsColumnMapping(BaseModel):
    timestamp: str
    open: str
    high: str
    low: str
    close: str
    volume: str
    symbol: str

    def as_rename_dict(self) -> dict[str, str]:
        # For use with pandas.DataFrame.rename(columns=...)
        return {v: k for k, v in self.model_dump().items()}


class BarsSchema(pa.DataFrameModel):
    __annotations__ = {
        StandardBarsColumns.timestamp: pd.DatetimeTZDtype('ns', 'UTC'),
        StandardBarsColumns.open: float,
        StandardBarsColumns.high: float,
        StandardBarsColumns.low: float,
        StandardBarsColumns.close: float,
        StandardBarsColumns.volume: int,
        StandardBarsColumns.symbol: str,
    }
