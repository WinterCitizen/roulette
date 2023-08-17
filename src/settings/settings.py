"""Module containing project settings."""
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Project settings."""

    HOST: str
    PORT: int
    MAX_MESSAGE_SIZE: int
    MESSAGE_PREFIX_SIZE: int
    MESSAGE_LENGTH_SIZE: int

    model_config = SettingsConfigDict(env_file=".env")
