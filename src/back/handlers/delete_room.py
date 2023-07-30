import dataclasses
from typing import Self

from src.back.interfaces.handlers import MessageHandlerInterface
from src.back.interfaces.io import WriteStreamInterface
from src.back.interfaces.room_registry import RoomRegistryInterface
    
    
@dataclasses.dataclass
class DeleteRoomHandler(MessageHandlerInterface[DeleteRoomMessage]):
    """Interface for delete room."""

    room_registry: RoomRegistryInterface

    async def handle(
            self: Self,
            message: DeleteRoomMessage,
            stream: WriteStreamInterface,
        ) -> None:
        """Delete room."""
        room_name = message.room_name
        
        room = self.room_registry.get_room(room_name)
        if not room:
            msg = f"Not found room with name {room_name}"
            raise TypeError(msg)

        if not room.get_users():
            await self.room_registry.delete_room(room)
