import logging

import pandas as pd
from pandera.typing.pandas import DataFrame

from service.data.bars_column_models import BarsSchema
from utlis.plotting.MAC_plotter import MovingAverageCrossoverPlotter

from .base_strategy import BaseStrategy, Signal


class MovingAverageCrossover(BaseStrategy):
    """
    A simple moving average crossover strategy.
    """

    strategy_name: str = 'MovingAverageCrossover'
    plotter: MovingAverageCrossoverPlotter | None = None
    short_window: int
    long_window: int

    def generate_signal(self, bars: DataFrame[BarsSchema]) -> Signal:
        logger = logging.getLogger(__name__)
        if bars is None or len(bars) < max(self.short_window, self.long_window):
            logger.warning(
                'Not enough bars to compute moving averages: got '
                + f'{len(bars) if bars is not None else 0}, '
                + f'required {max(self.short_window, self.long_window)}.'
            )
            return Signal.HOLD

        # Ensure bars are sorted by timestamp if the column exists
        if 'timestamp' in bars.columns:
            bars = bars.sort_values('timestamp')

        short_ma = bars['close'].rolling(window=self.short_window, min_periods=1).mean()
        long_ma = bars['close'].rolling(window=self.long_window, min_periods=1).mean()

        crossover = (short_ma > long_ma) & (short_ma.shift(1) <= long_ma.shift(1))
        crossunder = (short_ma < long_ma) & (short_ma.shift(1) >= long_ma.shift(1))

        signals = pd.Series(Signal.HOLD.value, index=bars.index)
        signals[crossover] = Signal.BUY.value
        signals[crossunder] = Signal.SELL.value

        if self.plotter is not None:
            self.plotter.plot_strategy(
                bars, crossover, crossunder, long_ma, short_ma, self.short_window, self.long_window
            )

        last_signal = signals.iloc[-1]
        if last_signal != Signal.HOLD.value:
            logger.info(f'Actionable signal for {bars["timestamp"].iloc[-1]}: {last_signal}')
            return Signal(last_signal)
        logger.info(f'No actionable signal for {bars["timestamp"].iloc[-1]}')
        return Signal.HOLD

    # todo: place order function
    # todo: backtesting framework, data loader, etc.
