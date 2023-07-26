"""Module containing room implementation."""
import dataclasses
from datetime import datetime
from typing import Self
from zoneinfo import ZoneInfo

from src.back.interfaces.room import RoomInterface


@dataclasses.dataclass
class Room(RoomInterface):
    """Room implementation."""

    name: str
    created_at: datetime = dataclasses.field(
        default_factory=lambda: datetime.now(ZoneInfo("UTC")),
    )

    def get_name(self: Self) -> str:
        """Get room name."""
        return self.name

    def get_creation_datetime(self: Self) -> datetime:
        """Get room creation datetime."""
        return self.created_at
