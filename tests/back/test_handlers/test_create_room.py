"""Module containing tests for create room handler."""
import zoneinfo
from asyncio import Lock
from datetime import datetime

import pytest

from src.back.handlers.create_room import CreateRoomHandler
from src.back.interfaces.values.room import Room
from src.back.interfaces.values.user import User
from src.back.message.create_room import CreateRoomMessage
from src.back.room_registry import RoomRegistry
from tests.back.fake.io import FakeWriteStream
from tests.back.fake.notification import FakeNotification


async def test_create_room_handler_creates_room() -> None:
    """Test should create room."""
    # Given:
    registry = RoomRegistry(rooms_lock=Lock())
    handler = CreateRoomHandler(room_registry=registry, notifier=FakeNotification())
    user = User(name="test")

    # When: handler writes a message
    message = CreateRoomMessage(
        name="new room",
        space=2,
        user=user,
        created_at=datetime.now(tz=zoneinfo.ZoneInfo("UTC")),
    )
    await handler.handle(message, stream=FakeWriteStream())

    # Then: we check that amount of rooms is 1
    rooms = await registry.get_rooms()
    assert len(rooms) == 1


def test_create_room_message_serializes_bytes() -> None:
    """Test create room message is successfully serialized and deserialized."""
    # Given:
    user = User(name="test")
    message = CreateRoomMessage(
        name="new room",
        space=2,
        user=user,
        created_at=datetime.now(tz=zoneinfo.ZoneInfo("UTC")),
    )

    # When: we try to serialize and deserialize message
    serialized_message = message.to_bytes()
    deserialized_message = message.from_bytes(serialized_message)

    # Then: we check that the initial message is exactly the same as deserialized message
    assert deserialized_message == message


def test_fail_create_room_with_invalid_space() -> None:
    """Test room cannot be created with invalid space."""
    # Given:

    # When: we attempt to create room with invalid space:
    # Then: we catch a ValueError with a message
    with pytest.raises(ValueError, match="Space cannot be"):
        Room(name="fail", space=0)
