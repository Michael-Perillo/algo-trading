from pydantic_settings import BaseSettings, SettingsConfigDict


class AlpacaTradingSettings(BaseSettings):
    APCA_API_KEY_ID: str | None = None
    APCA_API_SECRET_KEY: str | None = None
    APCA_API_BASE_URL: str = 'https://paper-api.alpaca.markets'

    model_config = SettingsConfigDict(env_file='.env', env_file_encoding='utf-8')


def get_alpaca_trading_settings() -> AlpacaTradingSettings:
    return AlpacaTradingSettings()


class AlpacaDataSettings(BaseSettings):
    APCA_API_KEY_ID: str | None = None
    APCA_API_SECRET_KEY: str | None = None
    APCA_API_BASE_URL: str = 'https://data.alpaca.markets'

    model_config = SettingsConfigDict(env_file='.env', env_file_encoding='utf-8')


def get_alpaca_data_settings() -> AlpacaDataSettings:
    return AlpacaDataSettings()
