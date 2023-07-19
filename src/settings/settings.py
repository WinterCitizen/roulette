"""Module containing project settings."""
from pathlib import Path

from pydantic import BaseSettings, Field


class Settings(BaseSettings):
    """Project settings."""

    HOST: str = Field(default="localhost")
    PORT: int = Field(default=8888)

    class Config:
        """Project configuration."""

        env_file = Path(__file__).resolve().parent.parent.parent / ".env"
        case_sensitive = True
        env_prefix = ""
