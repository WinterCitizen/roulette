"""Module containing fake implementation of room."""
import dataclasses
from datetime import datetime
from zoneinfo import ZoneInfo

from src.back.interfaces.values.room import Room
from src.back.interfaces.values.user import User


class FakeRoom(Room):
    """Fake room implementation."""

    name: str
    space: int
    users: dict[str, User] = dataclasses.field(
        default_factory=dict,
    )
    created_at: datetime = dataclasses.field(
        default_factory=lambda: datetime.now(ZoneInfo("UTC")),
    )
