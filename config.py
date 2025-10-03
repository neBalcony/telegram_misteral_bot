# config.py
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    MISTRAL_API_KEY: str
    TELEGRAM_BOT_TOKEN: str
    MISTRAL_MODEL: str = "mistral-large-latest"
    ADMIN_ID: int

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"  # чтобы не ругался на комментарии в .env
    )


settings = Settings()
