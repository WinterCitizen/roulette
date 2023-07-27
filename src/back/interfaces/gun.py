"""Module containing gun interface."""
from typing import Protocol, Self


class GunInterface(Protocol):
    """Interface for gun."""

    def shuffle(self: Self) -> None:
        """Shuffle gun clip."""
        raise NotImplementedError

    def fire(self: Self) -> bool:
        """Fire bullet."""
        raise NotImplementedError

    def get_clip(self: Self) -> list[int]:
        """Get clip."""
        raise NotImplementedError
