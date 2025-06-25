import pandas as pd
from pandera.typing.pandas import DataFrame

from trading_bot_mvp.service.data.bars_column_models import BarsSchema

from .base_strategy import BaseStrategy, Signal


class MovingAverageCrossover(BaseStrategy):
    """
    A simple moving average crossover strategy.
    """

    strategy_name: str = 'MovingAverageCrossover'
    short_window: int
    long_window: int

    def generate_signal(self, bars: DataFrame[BarsSchema]) -> Signal:
        """
        Given a DataFrame of bars, return the most recent actionable signal from the enum Signal.
        found in the provided data. If multiple signals are present, the latest one is returned.
        """
        if bars is None or len(bars) < max(self.short_window, self.long_window):
            return Signal.HOLD

        short_ma = bars['close'].rolling(window=self.short_window, min_periods=1).mean()
        long_ma = bars['close'].rolling(window=self.long_window, min_periods=1).mean()

        # Find all crossover/crossunder points in the provided data
        crossover = (short_ma > long_ma) & (short_ma.shift(1) <= long_ma.shift(1))
        crossunder = (short_ma < long_ma) & (short_ma.shift(1) >= long_ma.shift(1))

        # Use string values for the Series, but map back to Signal enum for return
        signals = pd.Series(Signal.HOLD.value, index=bars.index)
        signals[crossover] = Signal.BUY.value
        signals[crossunder] = Signal.SELL.value

        actionable = signals[signals != Signal.HOLD.value]
        if not actionable.empty:
            last_signal_str = actionable.iloc[-1]
            return Signal(last_signal_str)
        return Signal.HOLD
