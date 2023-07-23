"""Module containing room interface."""
from datetime import datetime
from typing import Protocol, Self


class RoomInterface(Protocol):
    """Room holding it's members."""

    def get_name(self: Self) -> str:
        """Get room name."""
        raise NotImplementedError

    def get_creation_datetime(self: Self) -> datetime:
        """Get room creation datetime."""
        raise NotImplementedError
