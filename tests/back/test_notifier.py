"""Module containing tests for notifications."""
from asyncio import Lock

from src.back.interfaces.values.connection import ConnectionRegistry
from src.back.message.room import RoomMessage
from src.back.notifier.notifier import Notification
from src.back.room_registry import RoomRegistry
from tests.back.fake.io import FakeWriteStream
from tests.back.fake.room import FakeRoom


async def test_notifier() -> None:
    """Test notifications write room messages to the stream."""
    # Given: a fake stream in connection registry
    stream = FakeWriteStream()
    connection_registry = ConnectionRegistry()
    connection_registry.store_connection(stream)

    # Given: a fake room in room registry
    room = FakeRoom(name="test_name", space=2)
    room_registry = RoomRegistry(rooms_lock=Lock())
    await room_registry.add_room(room)

    # When: we notify to all connections
    notifier = Notification(connection_registry=connection_registry, room_registry=room_registry)
    await notifier.notify()

    # Then: we check that we write data to the stream
    message_bytes = stream.write_bytes
    room_message = RoomMessage(**room.as_dict()).from_bytes(message_bytes)
    room_bytes = room_message.to_bytes()
    assert message_bytes == room_bytes
