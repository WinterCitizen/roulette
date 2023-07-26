"""Module containing handlers."""
import dataclasses
from typing import Self

from src.back.interfaces.handlers import MessageHandlerInterface
from src.back.interfaces.io import WriteStreamInterface
from src.back.interfaces.room_registry import RoomRegistryInterface
from src.back.message.create_room import CreateRoomMessage
from src.back.room import Room


@dataclasses.dataclass
class CreateRoomHandler(MessageHandlerInterface[CreateRoomMessage]):
    """Interface for create room."""

    room_registry: RoomRegistryInterface

    async def handle(
        self: Self,
        message: CreateRoomMessage,
        stream: WriteStreamInterface,
    ) -> None:
        """Create room."""
        room = Room(name=message.name)
        await self.room_registry.add_room(room)
