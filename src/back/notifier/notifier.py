"""Module containing notification implementation."""
import dataclasses
from typing import Protocol, Self

from src.back.interfaces.connection_registry import ConnectionRegistryInterface
from src.back.interfaces.room_registry import RoomRegistryInterface
from src.back.message.room import RoomMessage


class NotificationInterface(Protocol):
    """Interface for notification."""

    async def notify(self: Self) -> None:
        """Notify client about rooms' state."""
        raise NotImplementedError


@dataclasses.dataclass
class Notification(NotificationInterface):
    """Notifications implementation."""

    room_registry: RoomRegistryInterface
    connection_registry: ConnectionRegistryInterface

    async def notify(self: Self) -> None:
        """Notify client about rooms' state."""
        rooms = await self.room_registry.get_rooms()
        connections = self.connection_registry.get_connections()
        for connection in connections:
            for room in rooms:
                message = RoomMessage(**room.as_dict())

                await connection.write(message.to_bytes())
