import os
from typing import Any

import matplotlib.pyplot as plt
import pandas as pd
from pandera.typing import DataFrame
from pydantic import BaseModel

from service.data.bars_column_models import BarsSchema
from utlis.plotting.base_strategy_plotter import BaseStrategyPlotter


class MovingAverageCrossoverPlotter(BaseStrategyPlotter, BaseModel):
    def __init__(self, **kwargs: Any) -> None:
        super().__init__(strategy_name='MovingAverageCrossover', **kwargs)

    def plot_strategy(
        self,
        bars: DataFrame[BarsSchema],
        crossover: 'pd.Series[bool]',
        crossunder: 'pd.Series[bool]',
        long_ma: 'pd.Series[float]',
        short_ma: 'pd.Series[float]',
        short_window: int,
        long_window: int,
    ) -> None:
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

        save_path = os.path.join(self.figures_dir, f'{end_ts}.png')
        plt.figure(figsize=(14, 7))
        plt.plot(bars.index, bars['close'], label='Price', color='black')
        plt.plot(bars.index, short_ma, label=f'Short MA ({short_window})', color='blue')
        plt.plot(bars.index, long_ma, label=f'Long MA ({long_window})', color='red')
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
        pass
