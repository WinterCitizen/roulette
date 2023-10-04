"""Module containing tests for leave user from room handler."""
from asyncio import Lock

import pytest

from src.back.handlers.leave_room import LeaveRoomHandler
from src.back.interfaces.values.room import Room
from src.back.interfaces.values.user import User
from src.back.message.leave_room import LeaveRoomMessage
from src.back.room_registry import RoomRegistry
from tests.back.fake.io import FakeWriteStream
from tests.back.fake.notification import FakeNotification


async def test_leave_room_handler_delete_user() -> None:
    """Test should leave a user from a room."""
    # Given: an existing room with a user
    user = User(
        name="sponge_bob",
    )

    room = Room(
        name="bordel",
        space=2,
        users={"sponge_bob": user},
    )

    registry = RoomRegistry(
        rooms_lock=Lock(),
        rooms={"bordel": room},
    )

    # When: handler writes a message
    message = LeaveRoomMessage(
        room=room,
        user=user,
    )

    handler = LeaveRoomHandler(room_registry=registry, notifier=FakeNotification())
    await handler.handle(message, stream=FakeWriteStream())

    # Then: ensure the user is removed from the room
    assert len(room.users) == 0


async def test_leave_room_handler_failed_to_delete_room() -> None:
    """Test should fail because the room is not found."""
    # Given: a user and a non-existing room
    user = User(
        name="sponge_bob",
    )

    non_existing_room = Room(
        name="bordel",
        space=2,
        users={"sponge_bob": user},
    )

    registry = RoomRegistry(
        rooms_lock=Lock(),
    )

    # When: the handler handles a LeaveRoomMessage for a non-existing room
    message = LeaveRoomMessage(
        room=non_existing_room,
        user=user,
    )

    handler = LeaveRoomHandler(room_registry=registry, notifier=FakeNotification())

    # Then: an error is raised because room not found
    with pytest.raises(ValueError, match="There is no room"):
        await handler.handle(message, stream=FakeWriteStream())


async def test_leave_room_handler_failed_to_remove_user() -> None:
    """Test should fail because the user is not in the room."""
    # Given: a non-existing user and an existing room
    non_existing_user = User(name="")

    room = Room(
        name="bordel",
        space=2,
    )

    registry = RoomRegistry(
        rooms_lock=Lock(),
        rooms={"bordel": room},
    )

    # When: the handler handles a LeaveRoomMessage for a non-existing user
    message = LeaveRoomMessage(
        room=room,
        user=non_existing_user,
    )

    handler = LeaveRoomHandler(room_registry=registry, notifier=FakeNotification())

    # Then: an error is raised because user is not in room
    with pytest.raises(ValueError, match="is not in room"):
        await handler.handle(message, stream=FakeWriteStream())


def test_leave_room_handler_serializes_bytes() -> None:
    """Test join room message is successfully serialized and deserialized."""
    # Given:
    room = Room(name="room", space=2)
    user = User(name="user")
    message = LeaveRoomMessage(
        room=room,
        user=user,
    )

    # When: we try to serialize and deserialize message
    serialized_message = message.to_bytes()
    deserialized_message = message.from_bytes(serialized_message)

    # Then: we check that the initial message is exactly the same as deserialized message
    assert deserialized_message == message
