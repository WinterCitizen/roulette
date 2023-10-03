"""Module containing room message."""
import dataclasses
from datetime import datetime
from typing import Self
from zoneinfo import ZoneInfo

import msgpack

from src.back.interfaces.message import MessageInterface
from src.back.interfaces.values.user import User


@dataclasses.dataclass
class RoomMessage(MessageInterface):
    """Room message."""

    name: str
    space: int
    users: dict[str, User]
    created_at: datetime

    @classmethod
    def from_bytes(cls, message_bytes: bytes) -> Self:
        """Create message from bytes."""
        message_dict = msgpack.loads(message_bytes)

        return cls(
            name=message_dict["name"],
            space=message_dict["space"],
            users={name: User(name=name) for name in message_dict["users"]},
            created_at=datetime.fromtimestamp(
                message_dict["created_at"],
                tz=ZoneInfo("UTC"),
            ),
        )

    def to_bytes(self: Self) -> bytes:
        """Serialize message to bytes."""
        return msgpack.dumps(
            {
                "name": self.name,
                "space": self.space,
                "users": self.users,
                "created_at": datetime.timestamp(self.created_at),
            },
        )
