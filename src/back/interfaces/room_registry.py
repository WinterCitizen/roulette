"""Module containing room registry interface."""
from typing import Protocol, Self

from src.back.interfaces.values.room import Room


class RoomRegistryInterface(Protocol):
    """Registry storing existing game rooms."""

    async def get_rooms(self: Self) -> tuple[Room, ...]:
        """Get all stored rooms."""
        raise NotImplementedError

    async def get_room(self: Self, room_name: str) -> Room | None:
        """Get room by name."""
        raise NotImplementedError

    async def add_room(self: Self, room: Room) -> None:
        """Add room to registry."""
        raise NotImplementedError

    async def delete_room(self: Self, room: Room) -> None:
        """Remove room from registry."""
        raise NotImplementedError
