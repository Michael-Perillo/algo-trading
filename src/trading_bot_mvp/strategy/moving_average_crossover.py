import pandas as pd

from .base_strategy import BaseStrategy, Signal


class MovingAverageCrossover(BaseStrategy):
    """
    A simple moving average crossover strategy.
    """

    strategy_name: str = 'MovingAverageCrossover'
    short_window: int
    long_window: int

    def generate_signals(self, bars: pd.DataFrame) -> pd.DataFrame:
        signals_df = pd.DataFrame(index=bars.index)
        signals_df['signal'] = Signal.HOLD

        # Calculate moving averages
        short_ma = bars['close'].rolling(window=self.short_window, min_periods=1).mean()
        long_ma = bars['close'].rolling(window=self.long_window, min_periods=1).mean()

        # Generate signals
        signals_df.loc[short_ma > long_ma, 'signal'] = Signal.BUY.value
        signals_df.loc[short_ma < long_ma, 'signal'] = Signal.SELL.value

        return signals_df
