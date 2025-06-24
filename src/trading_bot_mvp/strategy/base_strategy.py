from abc import ABC, abstractmethod
from enum import Enum

from pandera.typing.pandas import DataFrame
from pydantic import BaseModel

from trading_bot_mvp.service.data.bars_column_models import BarsSchema


class Signal(Enum):
    """
    Enum for trading signals.
    """

    BUY = 1
    SELL = -1
    HOLD = 0


class BaseStrategy(ABC, BaseModel):
    """
    An abstract base class for a trading strategy.
    It's a Pydantic BaseModel to allow for easy parameter validation.
    """

    strategy_name: str

    @abstractmethod
    def generate_signal(self, bars: DataFrame[BarsSchema]) -> Signal:
        """
        Generates trading signals for a given set of historical bars.

        Args:
            bars: A pandas DataFrame with historical bar data, including
                  columns like 'open', 'high', 'low', 'close', 'volume'.

        Returns:
            A pandas DataFrame with a 'signal' column containing Signal enums.
            The index of the returned DataFrame should match the input 'bars' DataFrame.
        """
        pass

    class Config:
        arbitrary_types_allowed = True
