"""Module containing leave room message."""
import dataclasses
from datetime import datetime
from typing import Self
from zoneinfo import ZoneInfo

import msgpack

from src.back.interfaces.message import MessageInterface
from src.back.interfaces.values.room import Room
from src.back.interfaces.values.user import User


@dataclasses.dataclass
class LeaveRoomMessage(MessageInterface):
    """Leave room message."""

    room: Room
    user: User

    @classmethod
    def from_bytes(cls, message_bytes: bytes) -> Self:
        """Create message from bytes."""
        message_dict = msgpack.loads(message_bytes)
        created_at = message_dict["room"].pop("created_at")
        return cls(
            room=Room(
                **message_dict["room"],
                created_at=datetime.fromtimestamp(created_at, tz=ZoneInfo("UTC")),
            ),
            user=User(**message_dict["user"]),
        )

    def to_bytes(self: Self) -> bytes:
        """Serialize message to bytes."""
        return msgpack.dumps(
            {
                "room": {
                    "name": self.room.name,
                    "space": self.room.space,
                    "users": self.room.users,
                    "created_at": datetime.timestamp(self.room.created_at),
                },
                "user": self.user.as_dict(),
            },
        )
