import datetime as dt
from unittest.mock import MagicMock

import pytest

from orchestrator.default_orchestrator import DefaultOrchestrator as Orchestrator
from portfolio.allocation.default_allocator import DefaultAllocator
from portfolio.risk.default_risk import DefaultRisk as RiskManagement
from service.brokerage.base_brokerage_service import BaseBrokerageService
from service.data.base_dao import BaseDAO
from shared.model import OrderRequest
from strategy.base_strategy import BaseStrategy
from thesis.SMA_thesis import SMACrossoverThesis


class DummyThesis(SMACrossoverThesis):
    def __init__(self, name: str, orders: list[OrderRequest]) -> None:
        super().__init__(
            thesis_name=name,
            asset_universe=[],
            strategy=MagicMock(spec=BaseStrategy),
            risk_management=MagicMock(spec=RiskManagement),
            data_dao=MagicMock(spec=BaseDAO),
            brokerage_service=MagicMock(spec=BaseBrokerageService),
            allocator=DefaultAllocator(),
            start_timestamp=dt.datetime.now(dt.UTC),  # Not used in this dummy thesis
        )
        self._orders = orders

    def generate_order(self) -> 'list[OrderRequest]':
        return self._orders


@pytest.fixture
def dummy_brokerage() -> MagicMock:
    return MagicMock(spec=BaseBrokerageService)


@pytest.fixture
def dummy_dao() -> MagicMock:
    return MagicMock(spec=BaseDAO)


def test_orchestrator_calls_thesis_and_prints(
    monkeypatch: pytest.MonkeyPatch,
    dummy_brokerage: MagicMock,
    dummy_dao: MagicMock,
    capsys: pytest.CaptureFixture[str],
) -> None:
    order1 = MagicMock()
    order1.symbol = 'AAPL'
    order1.dict.return_value = {'symbol': 'AAPL', 'side': 'buy'}
    thesis = DummyThesis('TestThesis', [order1])
    orchestrator = Orchestrator(
        theses=[thesis], brokerage_service=dummy_brokerage, data_dao=dummy_dao
    )
    # Patch time.sleep to break after one loop
    monkeypatch.setattr('time.sleep', lambda x: (_ for _ in ()).throw(KeyboardInterrupt()))
    # Patch the infinite loop to break after one iteration
    with pytest.raises(KeyboardInterrupt):
        orchestrator.run(interval_seconds=0)
    out = capsys.readouterr().out
    assert 'Evaluating Thesis: TestThesis' in out
    assert 'Placing order for AAPL' in out


def test_orchestrator_handles_multiple_theses(
    monkeypatch: pytest.MonkeyPatch,
    dummy_brokerage: MagicMock,
    dummy_dao: MagicMock,
    capsys: pytest.CaptureFixture[str],
) -> None:
    order1 = MagicMock()
    order1.symbol = 'AAPL'
    order1.dict.return_value = {'symbol': 'AAPL', 'side': 'buy'}
    order2 = MagicMock()
    order2.symbol = 'MSFT'
    order2.dict.return_value = {'symbol': 'MSFT', 'side': 'sell'}
    thesis1 = DummyThesis('Thesis1', [order1])
    thesis2 = DummyThesis('Thesis2', [order2])
    orchestrator = Orchestrator(
        theses=[thesis1, thesis2], brokerage_service=dummy_brokerage, data_dao=dummy_dao
    )
    monkeypatch.setattr('time.sleep', lambda x: (_ for _ in ()).throw(KeyboardInterrupt()))
    with pytest.raises(KeyboardInterrupt):
        orchestrator.run(interval_seconds=0)
    out = capsys.readouterr().out
    assert 'Evaluating Thesis: Thesis1' in out
    assert 'Evaluating Thesis: Thesis2' in out
    assert 'Placing order for AAPL' in out
    assert 'Placing order for MSFT' in out
