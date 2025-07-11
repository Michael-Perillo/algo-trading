import pandas as pd
from pandera.typing import DataFrame

from service.data.bars_column_models import BarsSchema
from strategy.base_strategy import Signal
from strategy.moving_average_crossover import MovingAverageCrossover


def make_bars(close_prices: list[int]) -> 'DataFrame[BarsSchema]':
    df = pd.DataFrame({'close': close_prices})
    # Optionally, validate with BarsSchema if strict typing is needed
    return df  # type: ignore


def test_hold_when_not_enough_data() -> None:
    strat = MovingAverageCrossover(short_window=3, long_window=5)
    bars = make_bars([1, 2])
    assert strat.generate_signal(bars) == Signal.HOLD


def test_hold_when_no_crossover() -> None:
    strat = MovingAverageCrossover(short_window=2, long_window=3)
    bars = make_bars([1, 1, 1, 1, 1])
    assert strat.generate_signal(bars) == Signal.HOLD


def test_buy_signal_on_crossover() -> None:
    strat = MovingAverageCrossover(short_window=2, long_window=3)
    bars = make_bars([1, 1, 1, 2, 3])
    # Short MA crosses above long MA at the last bar
    assert strat.generate_signal(bars) == Signal.BUY


def test_sell_signal_on_crossunder() -> None:
    strat = MovingAverageCrossover(short_window=2, long_window=3)
    bars = make_bars([3, 3, 3, 2, 1])
    # Short MA crosses below long MA at the last bar
    assert strat.generate_signal(bars) == Signal.SELL


def test_returns_last_actionable_signal() -> None:
    strat = MovingAverageCrossover(short_window=2, long_window=3)
    # Crossover (buy) at bar 3, crossunder (sell) at bar 5
    bars = make_bars([1, 1, 1, 2, 3, 2, 1])
    assert strat.generate_signal(bars) == Signal.SELL
