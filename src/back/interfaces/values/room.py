"""Module containing room implementation."""
import dataclasses
from datetime import datetime
from typing import Any, Self
from zoneinfo import ZoneInfo

from src.back.interfaces.values.user import User


@dataclasses.dataclass
class Room:
    """Room implementation."""

    name: str
    space: int
    users: dict[str, User] = dataclasses.field(
        default_factory=dict,
    )
    created_at: datetime = dataclasses.field(
        default_factory=lambda: datetime.now(ZoneInfo("UTC")),
    )

    def __post_init__(self: Self) -> None:
        """Validate space."""
        if self.space <= 1:
            msg = "Space cannot be 1 or less"
            raise ValueError(msg)

    def add_user(self: Self, user: User) -> None:
        """Add user to room."""
        self.users.update({user.name: user})

    def as_dict(self: Self) -> dict[str, Any]:
        """Convert object to dict."""
        return {
            "name": self.name,
            "space": self.space,
            "users": self.users,
            "created_at": datetime.timestamp(self.created_at),
        }
