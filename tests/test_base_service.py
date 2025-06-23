import pytest
from pydantic import BaseModel

from trading_bot_mvp.service.base_service import BaseService


class DummyModel(BaseModel):
    foo: str
    bar: int


class TargetModel(BaseModel):
    baz: str
    qux: int


class DummyService(BaseService):
    def __init__(self) -> None:
        super().__init__(api_client=None)
        pass


@pytest.fixture
def dummy_service() -> DummyService:
    return DummyService()


def test_base_service(dummy_service: DummyService) -> None:
    service = dummy_service
    assert isinstance(service, DummyService)
    assert service.api_client is None
