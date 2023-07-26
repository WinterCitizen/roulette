"""Module containing handlers."""
import dataclasses
from datetime import datetime
from typing import Self
from zoneinfo import ZoneInfo

import msgpack

from src.back.interfaces.handlers import MessageHandlerInterface
from src.back.interfaces.io import WriteStreamInterface
from src.back.interfaces.message import MessageInterface
from src.back.interfaces.room_registry import RoomRegistryInterface
from src.back.room import Room


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
            created_at=datetime.fromtimestamp(message_dict["created_at"], tz=ZoneInfo("UTC")),
        )

    def to_bytes(self: Self) -> bytes:
        """Serialize message to bytes."""
        return msgpack.dumps({"name": self.name, "created_at": datetime.timestamp(self.created_at)})


@dataclasses.dataclass
class CreateRoomHandler(MessageHandlerInterface[CreateRoomMessage]):
    """Interface for create room."""

    room_registry: RoomRegistryInterface

    async def handle(self: Self, message: CreateRoomMessage, stream: WriteStreamInterface) -> None:
        """Create room."""
        room = Room(name=message.name)
        self.room_registry.add_room(room)
