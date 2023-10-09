import dataclasses
from typing import Self

from src.back.interfaces.handlers import MessageHandlerInterface
from src.back.interfaces.io import WriteStreamInterface
from src.back.interfaces.room_registry import RoomRegistryInterface
from src.back.notifier.notifier import NotificationInterface
from src.back.message.list_room import ListRoomsMessage


@dataclasses.dataclass
class ListRoomsHandler(MessageHandlerInterface[ListRoomsMessage]):
    """Interface for list of rooms."""

    room_registry: RoomRegistryInterface
    notifier: NotificationInterface

    async def handle(
        self: Self,
        message: ListRoomsMessage,
        stream: WriteStreamInterface,
    ) -> None:
        """List rooms."""
        await self.notifier.notify()
