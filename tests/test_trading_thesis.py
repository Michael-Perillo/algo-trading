from unittest.mock import MagicMock

import pytest
from pandera.typing.pandas import DataFrame

from service.brokerage.base_brokerage_service import BaseBrokerageService
from service.data.bars_column_models import BarsSchema
from service.data.base_dao import BaseDAO
from shared.model import OrderRequest
from strategy.base_strategy import BaseStrategy, Signal
from thesis.trading_thesis import RiskManagement, TradingThesis


class DummyStrategy_BUY(BaseStrategy):
    strategy_name: str = 'DummyStrategy'

    def generate_signal(self, bars: DataFrame[BarsSchema]) -> Signal:
        # Always return a buy signal for testing
        return Signal.BUY


class DummyStrategy_SELL(BaseStrategy):
    strategy_name: str = 'DummyStrategy'

    def generate_signal(self, bars: DataFrame[BarsSchema]) -> Signal:
        # Always return a buy signal for testing
        return Signal.SELL


@pytest.fixture
def dummy_brokerage() -> MagicMock:
    brokerage = MagicMock(spec=BaseBrokerageService)
    brokerage.get_account.return_value = MagicMock()
    brokerage.get_open_positions.return_value = []
    return brokerage


@pytest.fixture
def dummy_dao() -> MagicMock:
    dao = MagicMock(spec=BaseDAO)
    dao.get_bars.return_value = MagicMock()
    return dao


@pytest.fixture
def trading_thesis_BUY(dummy_brokerage: MagicMock, dummy_dao: MagicMock) -> TradingThesis:
    return TradingThesis(
        thesis_name='Test Thesis',
        asset_universe=['AAPL', 'MSFT'],
        strategy=DummyStrategy_BUY(),
        risk_management=RiskManagement(),
        data_dao=dummy_dao,
        brokerage_service=dummy_brokerage,
    )


def test_generate_order_calls_dependencies_BUY(
    trading_thesis_BUY: TradingThesis, dummy_brokerage: MagicMock, dummy_dao: MagicMock
) -> None:
    orders = trading_thesis_BUY.generate_order()
    assert isinstance(orders, list)
    assert all(isinstance(order, OrderRequest) for order in orders)
    assert dummy_brokerage.get_account.called
    assert dummy_brokerage.get_open_positions.called
    assert dummy_dao.get_bars.call_count == len(trading_thesis_BUY.asset_universe)


@pytest.fixture
def trading_thesis_SELL(dummy_brokerage: MagicMock, dummy_dao: MagicMock) -> TradingThesis:
    return TradingThesis(
        thesis_name='Test Thesis',
        asset_universe=['AAPL', 'MSFT'],
        strategy=DummyStrategy_SELL(),
        risk_management=RiskManagement(),
        data_dao=dummy_dao,
        brokerage_service=dummy_brokerage,
    )


def test_generate_order_calls_dependencies_SELL(
    trading_thesis_SELL: TradingThesis, dummy_brokerage: MagicMock, dummy_dao: MagicMock
) -> None:
    orders = trading_thesis_SELL.generate_order()
    assert isinstance(orders, list)
    assert all(isinstance(order, OrderRequest) for order in orders)
    assert dummy_brokerage.get_account.called
    assert dummy_brokerage.get_open_positions.called
    assert dummy_dao.get_bars.call_count == len(trading_thesis_SELL.asset_universe)


def test_generate_order_handles_no_assets(trading_thesis_BUY: TradingThesis) -> None:
    trading_thesis_BUY.asset_universe = []
    orders = trading_thesis_BUY.generate_order()
    assert orders == []
