"""Module containing room registry interface."""
from typing import Protocol, Self

from back.interfaces.room import RoomInterface


class RoomRegistryInterface(Protocol):
    """Registry storing existing game rooms."""

    def get_rooms(self: Self) -> tuple[RoomInterface, ...]:
        """Get all stored rooms."""
        raise NotImplementedError

    def get_room(self: Self, room_name: str) -> RoomInterface | None:
        """Get room by name."""
        raise NotImplementedError

    def add_room(self: Self, room: RoomInterface) -> None:
        """Add room to registry."""
        raise NotImplementedError

    def delete_room(self: Self, room: RoomInterface) -> None:
        """Remove room from registry."""
        raise NotImplementedError

