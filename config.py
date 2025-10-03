# config.py
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import field_validator


class Settings(BaseSettings):
    MISTRAL_API_KEY: str
    TELEGRAM_BOT_TOKEN: str
    MISTRAL_MODEL: str = "mistral-large-latest"
    ADMIN_ID: list[int]  # список ID админов

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"  # чтобы не ругался на комментарии в .env
    )

    @field_validator("ADMIN_ID", mode="before")
    def split_admins(cls, v):
        if isinstance(v, str):
            return [int(x.strip()) for x in v.split(",")]
        return v


settings = Settings()
