"""Module containing handler for joining room."""
import dataclasses
from typing import Self

from src.back.interfaces.handlers import MessageHandlerInterface
from src.back.interfaces.io import WriteStreamInterface
from src.back.interfaces.room_registry import RoomRegistryInterface
from src.back.message.join_room import JoinRoomMessage
from src.back.notifier.notifier import NotificationInterface


@dataclasses.dataclass
class JoinRoomHandler(MessageHandlerInterface[JoinRoomMessage]):
    """Interface for create room."""

    room_registry: RoomRegistryInterface
    notifier: NotificationInterface

    async def handle(
        self: Self,
        message: JoinRoomMessage,
        stream: WriteStreamInterface,
    ) -> None:
        """Join room."""
        room = await self.room_registry.get_room(message.room.name)
        if not room:
            msg = f"There is no room with name {message.room.name}"
            raise ValueError(msg)

        if room.space == len(room.users):
            msg = "Room is already full"
            raise ValueError(msg)

        room.add_user(message.user)

        await self.notifier.notify()
