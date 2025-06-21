import pytest
from pydantic import BaseModel
from trading_bot_mvp.service.base_service import BaseService
from trading_bot_mvp.shared.model import FieldMap


class DummyModel(BaseModel):
    foo: str
    bar: int


class TargetModel(BaseModel):
    baz: str
    qux: int


class DummyService(BaseService):
    def __init__(self):
        pass


@pytest.fixture
def dummy_service():
    return DummyService()


def test_map_model_identity(dummy_service):
    src = DummyModel(foo='hello', bar=42)
    tgt = dummy_service.map_model(
        src, TargetModel, FieldMap(mapping={'baz': 'foo', 'qux': 'bar'})
    )
    assert tgt.baz == 'hello'
    assert tgt.qux == 42
