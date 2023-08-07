"""Module containing room registry."""
import dataclasses
from asyncio import Lock
from typing import Self

from src.back.interfaces.room_registry import RoomRegistryInterface
from src.back.interfaces.values.room import Room


@dataclasses.dataclass
class RoomRegistry(RoomRegistryInterface):
    """Registry storing game rooms."""

    rooms_lock: Lock
    rooms: dict[str, Room] = dataclasses.field(default_factory=dict)

    async def get_rooms(self: Self) -> tuple[Room, ...]:
        """Get all stored rooms."""
        return tuple(
            sorted(self.rooms.values(), key=lambda room: room.created_at),
        )

    async def get_room(self: Self, room_name: str) -> Room | None:
        """Get room by name."""
        return self.rooms.get(room_name)

    async def add_room(self: Self, room: Room) -> None:
        """Add room to registry."""
        async with self.rooms_lock:
            if room.name in self.rooms:
                msg = f"Room {room.name} already exists"
                raise ValueError(msg)

            self.rooms[room.name] = room

    async def delete_room(self: Self, room: Room) -> None:
        """Delete room from registry."""
        async with self.rooms_lock:
            if room.name not in self.rooms:
                msg = f"Room {room.name} doesn't exist"
                raise ValueError(msg)

            self.rooms.pop(room.name)
