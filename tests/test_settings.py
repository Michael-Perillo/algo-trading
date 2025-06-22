from collections.abc import Generator

import pytest
from pydantic_settings import SettingsConfigDict

from trading_bot_mvp.settings import Settings

PytestGeneratorFixture = Generator[None]


class SettingsForTest(Settings):
    model_config = SettingsConfigDict(env_file=None)


def get_settings() -> SettingsForTest:
    """
    Returns an instance of the Settings class.
    This function can be used to override the default settings for testing purposes.
    """
    return SettingsForTest()


@pytest.fixture
def env_api_keys(monkeypatch: pytest.MonkeyPatch) -> PytestGeneratorFixture:
    monkeypatch.setenv('API_KEY', 'test_api_key')
    monkeypatch.setenv('SECRET_KEY', 'test_secret_key')
    yield
    monkeypatch.delenv('API_KEY', raising=False)
    monkeypatch.delenv('SECRET_KEY', raising=False)


@pytest.fixture
def env_base_url(monkeypatch: pytest.MonkeyPatch) -> PytestGeneratorFixture:
    monkeypatch.setenv('BASE_URL', 'https://test-url.com')
    yield
    monkeypatch.delenv('BASE_URL', raising=False)


@pytest.mark.usefixtures('monkeypatch')
def test_settings_loads_env(
    env_api_keys: PytestGeneratorFixture, env_base_url: PytestGeneratorFixture
) -> None:
    settings = get_settings()
    assert settings.API_KEY == 'test_api_key'
    assert settings.SECRET_KEY == 'test_secret_key'
    assert settings.BASE_URL == 'https://test-url.com'


def test_settings_default_base_url(
    env_api_keys: PytestGeneratorFixture, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.delenv('BASE_URL', raising=False)
    settings = get_settings()
    assert settings.BASE_URL == 'https://paper-api.alpaca.markets'
