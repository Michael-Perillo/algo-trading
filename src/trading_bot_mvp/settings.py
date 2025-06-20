from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    """
    Defines the application's configuration settings.
    Pydantic automatically reads values from environment variables
    and the specified .env file.
    """
    # This tells Pydantic to load from a .env file
    model_config = SettingsConfigDict(env_file='.env', env_file_encoding='utf-8')

    # --- API Credentials (loaded from .env file) ---
    API_KEY: str
    SECRET_KEY: str

    # --- Broker Configuration ---
    BASE_URL: str = "https://paper-api.alpaca.markets"

    # --- Data Configuration ---
    DATA_BASE_URL: str = "https://data.alpaca.markets"

# Create a single, importable instance of the settings
def get_settings():
    return Settings()