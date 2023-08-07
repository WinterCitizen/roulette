"""Module testing room registry."""
from asyncio import Lock

import pytest

from src.back.room_registry import RoomRegistry
from tests.back.fake.room import FakeRoom


async def test_room_registry() -> None:
    """Test that room works."""
    # Given:
    room_registry = RoomRegistry(rooms_lock=Lock())

    room = FakeRoom(name="test_name", space=2)

    # When: room is added to the registry
    await room_registry.add_room(room)

    # Then: it can be fetched by name & all rooms is a tuple of a single added room
    assert await room_registry.get_room(room.name) == room
    assert await room_registry.get_rooms() == (room,)


async def test_room_registry_already_exists() -> None:
    """Test that you can't add rooms with the same names."""
    # Given: room registry with added room
    room_registry = RoomRegistry(rooms_lock=Lock())

    room = FakeRoom(name="test_name", space=2)

    await room_registry.add_room(room)

    # When: you try to add a room with the same name
    # Then: an error is raised
    with pytest.raises(ValueError, match="already exists"):
        await room_registry.add_room(room)


async def test_room_registry_deletion() -> None:
    """Test that room can be deleted from the registry."""
    # Given: registry with existing room
    room_registry = RoomRegistry(rooms_lock=Lock())

    room = FakeRoom(name="test_name", space=2)

    await room_registry.add_room(room)

    # When: the room is deleted from the registry
    await room_registry.delete_room(room)

    # Then: the room is no longer there 😁
    assert await room_registry.get_room(room.name) is None


async def test_room_registry_deletion_fails() -> None:
    """Test that registry raises an error when not stored room is deleted."""
    # Given: an empty registry
    room_registry = RoomRegistry(rooms_lock=Lock())

    room = FakeRoom(name="test_name", space=2)

    # When: you try to delete not stored room
    # Then: an error is raised
    with pytest.raises(ValueError, match="doesn't exist"):
        await room_registry.delete_room(room)
