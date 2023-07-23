"""Module containing room registry."""
import dataclasses
from threading import Lock
from typing import Self

from back.interfaces.room import RoomInterface
from back.interfaces.room_registry import RoomRegistryInterface


@dataclasses.dataclass
class RoomRegistry(RoomRegistryInterface):
    """Registry storing game rooms."""

    rooms_lock: Lock
    rooms: dict[str, RoomInterface] = dataclasses.field(default_factory=dict)

    def get_rooms(self: Self) -> tuple[RoomInterface, ...]:
        """Get all stored rooms."""
        return tuple(sorted(self.rooms.values(), key=lambda room: room.get_creation_datetime()))

    def get_room(self: Self, room_name: str) -> RoomInterface | None:
        """Get room by name."""
        return self.rooms.get(room_name)

    def add_room(self: Self, room: RoomInterface) -> None:
        """Add room to registry."""
        room_name = room.get_name()

        with self.rooms_lock:
            if room_name in self.rooms:
                msg = f"Room {room_name} already exists"
                raise ValueError(msg)

            self.rooms[room_name] = room

    def delete_room(self: Self, room: RoomInterface) -> None:
        """Delete room from registry."""
        room_name = room.get_name()

        with self.rooms_lock:
            if room_name not in self.rooms:
                msg = f"Room {room_name} doesn't exist"
                raise ValueError(msg)

            self.rooms.pop(room_name)