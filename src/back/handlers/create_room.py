"""Module containing handler for creating room."""
import dataclasses
from typing import Self

from src.back.interfaces.handlers import MessageHandlerInterface
from src.back.interfaces.io import WriteStreamInterface
from src.back.interfaces.room_registry import RoomRegistryInterface
from src.back.interfaces.values.room import Room
from src.back.interfaces.values.user import User
from src.back.message.create_room import CreateRoomMessage


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
        room = Room(name=message.name, space=message.space)
        await self.room_registry.add_room(room)

        user = User(name=message.user.name)
        room.add_user(user)
