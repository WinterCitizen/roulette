"""Module testing room registry."""
import dataclasses
from datetime import datetime
from threading import Lock
from typing import Self
from zoneinfo import ZoneInfo

import pytest

from src.back.interfaces.room import RoomInterface
from src.back.room_registry import RoomRegistry


@dataclasses.dataclass
class FakeRoom(RoomInterface):
    """Fake room implementation."""

    name: str
    created_at: datetime = dataclasses.field(default_factory=lambda: datetime.now(ZoneInfo("UTC")))

    def get_name(self: Self) -> str:
        """Get room name."""
        return self.name

    def get_creation_datetime(self: Self) -> datetime:
        """Get room creation datetime."""
        return self.created_at


def test_room_registry() -> None:
    """Test that room works."""
    # Given:
    room_registry = RoomRegistry(rooms_lock=Lock())

    room = FakeRoom(name="test_name")

    # When: room is added to the registry
    room_registry.add_room(room)

    # Then: it can be fetched by name & all rooms is a tuple of a single added room
    assert room_registry.get_room(room.get_name()) == room
    assert room_registry.get_rooms() == (room,)


def test_room_registry_already_exists() -> None:
    """Test that you can't add rooms with the same names."""
    # Given: room registry with added room
    room_registry = RoomRegistry(rooms_lock=Lock())

    room = FakeRoom(name="test_name")

    room_registry.add_room(room)

    # When: you try to add a room with the same name
    # Then: an error is raised
    with pytest.raises(ValueError, match="already exists"):
        room_registry.add_room(room)


def test_room_registry_deletion() -> None:
    """Test that room can be deleted from the registry."""
    # Given: registry with existing room
    room_registry = RoomRegistry(rooms_lock=Lock())

    room = FakeRoom(name="test_name")

    room_registry.add_room(room)

    # When: the room is deleted from the registry
    room_registry.delete_room(room)

    # Then: the room is no longer there 😁
    assert room_registry.get_room(room.get_name()) is None


def test_room_registry_deletion_fails() -> None:
    """Test that registry raises an error when not stored room is deleted."""
    # Given: an empty registry
    room_registry = RoomRegistry(rooms_lock=Lock())

    room = FakeRoom(name="test_name")

    # When: you try to delete not stored room
    # Then: an error is raised
    with pytest.raises(ValueError, match="doesn't exist"):
        room_registry.delete_room(room)
