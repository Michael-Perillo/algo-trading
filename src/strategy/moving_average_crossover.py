import logging
import os

import matplotlib.pyplot as plt
import pandas as pd
from pandera.typing.pandas import DataFrame

from service.data.bars_column_models import BarsSchema

from .base_strategy import BaseStrategy, Signal


class MovingAverageCrossover(BaseStrategy):
    """
    A simple moving average crossover strategy.
    """

    strategy_name: str = 'MovingAverageCrossover'
    short_window: int
    long_window: int

    def generate_signal(self, bars: DataFrame[BarsSchema], plot: bool = True) -> Signal:
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

        if plot:
            self.plot_crossovers(bars, crossover, crossunder, long_ma, short_ma)

        last_signal = signals.iloc[-1]
        if last_signal != Signal.HOLD.value:
            logger.info(f'Actionable signal for {bars["timestamp"].iloc[-1]}: {last_signal}')
            return Signal(last_signal)
        logger.info(f'No actionable signal for {bars["timestamp"].iloc[-1]}')
        return Signal.HOLD

    def plot_crossovers(
        self,
        bars: DataFrame[BarsSchema],
        crossover: 'pd.Series[bool]',
        crossunder: 'pd.Series[bool]',
        long_ma: 'pd.Series[float]',
        short_ma: 'pd.Series[float]',
    ) -> None:
        figures_dir = f'{self.strategy_name}_figures'
        os.makedirs(figures_dir, exist_ok=True)
        timestamps = bars['timestamp']
        start_ts = timestamps.iloc[0]
        end_ts = timestamps.iloc[-1]
        # Try to infer frequency
        freq = pd.infer_freq(timestamps)
        if freq is None and len(timestamps) > 1:
            freq = str(pd.Series(timestamps).diff().mode()[0])
        else:
            freq = str(freq) if freq is not None else 'unknown'
        freq_str = freq

        save_path = os.path.join(figures_dir, f'{end_ts}.png')
        plt.figure(figsize=(14, 7))
        plt.plot(bars.index, bars['close'], label='Price', color='black')
        plt.plot(bars.index, short_ma, label=f'Short MA ({self.short_window})', color='blue')
        plt.plot(bars.index, long_ma, label=f'Long MA ({self.long_window})', color='red')
        plt.scatter(
            bars.index[crossover],
            bars['close'][crossover],
            marker='^',
            color='green',
            label='Buy Signal',
            zorder=5,
        )
        plt.scatter(
            bars.index[crossunder],
            bars['close'][crossunder],
            marker='v',
            color='red',
            label='Sell Signal',
            zorder=5,
        )
        plt.legend()
        plt.title('Moving Average Crossover Signals')
        plt.xlabel('Bar #')
        plt.ylabel('Price')
        plt.grid(True)
        # Annotate with start/end/frequency
        annotation = (
            f'Symbol: {bars["symbol"][0]}\nStart: {start_ts}\nEnd: {end_ts}\nFreq: {freq_str}'
        )
        plt.gcf().text(
            0.99,
            0.01,
            annotation,
            fontsize=10,
            ha='right',
            va='bottom',
            bbox=dict(facecolor='white', alpha=0.7, edgecolor='gray'),
        )
        plt.tight_layout()
        plt.savefig(save_path)
        plt.close()
