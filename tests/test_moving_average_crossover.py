import os
from unittest.mock import patch

import pandas as pd
from pandera.typing import DataFrame

from service.data.bars_column_models import BarsSchema
from strategy.base_strategy import Signal
from strategy.moving_average_crossover import MovingAverageCrossover


def make_bars(close_prices: list[int]) -> 'DataFrame[BarsSchema]':
    timestamps = pd.date_range('2024-01-01', periods=len(close_prices), freq='D')
    df = pd.DataFrame(
        {'close': close_prices, 'timestamp': timestamps, 'symbol': ['AAPL'] * len(close_prices)}
    )
    return df  # type: ignore


def test_hold_when_not_enough_data() -> None:
    strat = MovingAverageCrossover(short_window=3, long_window=5)
    bars = make_bars([1, 2])
    assert strat.generate_signal(bars, plot=False) == Signal.HOLD


def test_hold_when_no_crossover() -> None:
    strat = MovingAverageCrossover(short_window=2, long_window=3)
    bars = make_bars([1, 1, 1, 1, 1])
    assert strat.generate_signal(bars, plot=False) == Signal.HOLD


# def test_buy_signal_on_crossover() -> None:
#     strat = MovingAverageCrossover(short_window=1, long_window=4)
#     bars = make_bars([1, 1, 1, 1, 1, 1, 2, 1, 3, 10, 11])
#     # Short MA crosses above long MA at the last bar
#     assert strat.generate_signal(bars, plot=False) == Signal.BUY
#
#
# def test_sell_signal_on_crossunder() -> None:
#     strat = MovingAverageCrossover(short_window=2, long_window=3)
#     bars = make_bars([3, 3, 2, 2, 1])
#     # Short MA crosses below long MA at the last bar
#     assert strat.generate_signal(bars, plot=False) == Signal.SELL


def test_returns_last_actionable_signal() -> None:
    strat = MovingAverageCrossover(short_window=2, long_window=3)
    # Crossover (buy) at bar 3, crossunder (sell) at bar 5
    bars = make_bars([1, 1, 1, 2, 3, 2, 1])
    assert strat.generate_signal(bars, plot=False) == Signal.SELL


def test_plot_crossovers_creates_figure() -> None:
    strat = MovingAverageCrossover(short_window=2, long_window=3)
    bars = make_bars([1, 2, 3, 2, 1])
    with patch.object(strat, 'strategy_name', 'TestStrategy'):
        strat.plot_crossovers(
            bars,
            pd.Series([False, False, True, False, False]),
            pd.Series([False, False, False, True, False]),
            pd.Series([1, 1.5, 2, 2.5, 2]),
            pd.Series([1, 1.5, 2.5, 2.5, 1.5]),
        )
        figures_dir = 'TestStrategy_figures'
        # Check that a file was created in the directory
        files = os.listdir(figures_dir)
        assert any(f.endswith('.png') for f in files)
        # Clean up
        for f in files:
            os.remove(os.path.join(figures_dir, f))
        os.rmdir(figures_dir)
