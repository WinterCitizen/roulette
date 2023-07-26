"""Module containing create room message."""
import dataclasses
from datetime import datetime
from typing import Self
from zoneinfo import ZoneInfo

import msgpack

from src.back.interfaces.message import MessageInterface


@dataclasses.dataclass
class CreateRoomMessage(MessageInterface):
    """Create room message."""

    name: str
    created_at: datetime

    @classmethod
    def from_bytes(cls, message_bytes: bytes) -> Self:
        """Create message from bytes."""
        message_dict = msgpack.loads(message_bytes)

        return cls(
            name=message_dict["name"],
            created_at=datetime.fromtimestamp(
                message_dict["created_at"],
                tz=ZoneInfo("UTC"),
            ),
        )

    def to_bytes(self: Self) -> bytes:
        """Serialize message to bytes."""
        return msgpack.dumps(
            {"name": self.name, "created_at": datetime.timestamp(self.created_at)},
        )
