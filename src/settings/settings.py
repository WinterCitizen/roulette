"""Module containing project settings."""
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Project settings."""

    HOST: str
    PORT: int

    model_config = SettingsConfigDict(env_file=".env")
