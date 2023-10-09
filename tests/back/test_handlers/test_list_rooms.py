from src.back.handlers.list_room_handler import ListRoomsHandler
from asyncio import Lock


from src.back.interfaces.values.room import Room
from src.back.message.list_room import ListRoomsMessage
from src.back.message.room import RoomMessage
from src.back.room_registry import RoomRegistry
from tests.back.fake.io import FakeWriteStream
from tests.back.fake.notification import FakeNotification


async def test_list_rooms() -> None:
    """Test should join user to room."""
    # Given: an existing room
    registry = RoomRegistry(rooms_lock=Lock())

    room = Room(
        name="bordel",
        space=2,
    )
    await registry.add_room(room)

    room = Room(
        name="hotel",
        space=2,
    )

    await registry.add_room(room)

    message = ListRoomsMessage()
    handler = ListRoomsHandler(room_registry=registry, notifier=FakeNotification())
    await handler.handle(message=message, stream=FakeWriteStream())
