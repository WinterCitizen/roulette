"""Module containing pytest fixtures."""
import pytest

from src.back.dependencies import wire_dependencies


@pytest.fixture(autouse=True)
def _configure_dependencies() -> None:
    """Wire dependencies to modules."""
    wire_dependencies()
