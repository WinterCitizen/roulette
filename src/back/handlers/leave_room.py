"""Module containing handler for leaving room."""
import dataclasses
from typing import Self

from src.back.interfaces.handlers import MessageHandlerInterface
from src.back.interfaces.io import WriteStreamInterface
from src.back.interfaces.room_registry import RoomRegistryInterface
from src.back.message.leave_room import LeaveRoomMessage
from src.back.notifier.notifier import NotificationInterface


@dataclasses.dataclass
class LeaveRoomHandler(MessageHandlerInterface[LeaveRoomMessage]):
    """Handler for leaving room."""

    room_registry: RoomRegistryInterface
    notifier: NotificationInterface

    async def handle(self: Self, message: LeaveRoomMessage, stream: WriteStreamInterface) -> None:
        """Handle the leave room message."""
        room = await self.room_registry.get_room(message.room.name)
        if not room:
            msg = f"There is no room with name {message.room.name}"
            raise ValueError(msg)

        user_name = message.user.name

        if user_name not in room.users:
            msg = f"User '{user_name}' is not in room '{room}'"
            raise ValueError(msg)

        room.remove_user(user_name)

        if len(room.users.keys()) == 0:
            await self.room_registry.delete_room(room)
