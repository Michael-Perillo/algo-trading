import pytest
from pydantic import ValidationError
from trading_bot_mvp.settings import Settings

@pytest.fixture
def env_api_keys(monkeypatch):
    monkeypatch.setenv("API_KEY", "test_api_key")
    monkeypatch.setenv("SECRET_KEY", "test_secret_key")
    yield
    monkeypatch.delenv("API_KEY", raising=False)
    monkeypatch.delenv("SECRET_KEY", raising=False)

@pytest.fixture
def env_base_url(monkeypatch):
    monkeypatch.setenv("BASE_URL", "https://test-url.com")
    yield
    monkeypatch.delenv("BASE_URL", raising=False)


def test_settings_loads_env(env_api_keys, env_base_url):
    settings = Settings()
    assert settings.API_KEY == "test_api_key"
    assert settings.SECRET_KEY == "test_secret_key"
    assert settings.BASE_URL == "https://test-url.com"


def test_settings_default_base_url(env_api_keys, monkeypatch):
    monkeypatch.delenv("BASE_URL", raising=False)
    settings = Settings()
    assert settings.BASE_URL == "https://paper-api.alpaca.markets"

@pytest.mark.usefixtures("monkeypatch")
def test_settings_missing_required(monkeypatch):
    monkeypatch.delenv("API_KEY", raising=False)
    monkeypatch.delenv("SECRET_KEY", raising=False)
    with pytest.raises(ValidationError):
        Settings()
