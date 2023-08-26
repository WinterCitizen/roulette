"""Module containing tests for join room handler."""
from asyncio import Lock

import pytest

from src.back.handlers.join_room import JoinRoomHandler
from src.back.interfaces.values.room import Room
from src.back.interfaces.values.user import User
from src.back.message.join_room import JoinRoomMessage
from src.back.room_registry import RoomRegistry
from tests.back.fake.io import FakeWriteStream
from tests.back.fake.notification import FakeNotification


async def test_join_room_handler_joins_user_to_room() -> None:
    """Test should join user to room."""
    # Given: an existing room
    registry = RoomRegistry(rooms_lock=Lock())
    room = Room(
        name="bordel",
        space=2,
    )
    await registry.add_room(room)

    # When: handler writes a message
    handler = JoinRoomHandler(room_registry=registry, notifier=FakeNotification())

    user = User(name="test")
    message = JoinRoomMessage(
        room=room,
        user=user,
    )
    await handler.handle(message, stream=FakeWriteStream())

    # Then: we check that amount of users in a room is 1
    assert len(room.users) == 1


async def test_fail_join_room_not_found() -> None:
    """Test should not let user join room because the room not found."""
    # Given:
    registry = RoomRegistry(rooms_lock=Lock())

    # When: user attemts to join a room with non-existing name
    join_handler = JoinRoomHandler(room_registry=registry, notifier=FakeNotification())
    join_message = JoinRoomMessage(
        room=Room(name="room", space=2),
        user=User(name="user"),
    )

    # Then: an error is raised because room not found
    with pytest.raises(ValueError, match="There is no room"):
        await join_handler.handle(join_message, stream=FakeWriteStream())


async def test_fail_join_room_not_enough_space() -> None:
    """Test should not let user join room because the room is full."""
    # Given: a 2 space room with 2 users already in a room
    registry = RoomRegistry(rooms_lock=Lock())

    room = Room(
        name="house",
        space=2,
        users={
            "name": User(name="user"),
            "name2": User(name="name2"),
        },
    )
    await registry.add_room(room)

    # When: third user attemts to join a full room
    join_handler = JoinRoomHandler(room_registry=registry, notifier=FakeNotification())
    join_message = JoinRoomMessage(
        room=room,
        user=User(name="third"),
    )

    # Then: an error is raised because room not found
    with pytest.raises(ValueError, match="is already full"):
        await join_handler.handle(join_message, stream=FakeWriteStream())


def test_join_room_message_serializes_bytes() -> None:
    """Test join room message is successfully serialized and deserialized."""
    # Given:
    room = Room(name="room", space=2)
    user = User(name="user")
    message = JoinRoomMessage(
        room=room,
        user=user,
    )

    # When: we try to serialize and deserialize message
    serialized_message = message.to_bytes()
    deserialized_message = message.from_bytes(serialized_message)

    # Then: we check that the initial message is exactly the same as deserialized message
    assert deserialized_message == message
