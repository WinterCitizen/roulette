import dataclasses
import msgpack

from typing import Self

from src.back.interfaces.message import MessageInterface


@dataclasses.dataclass
class DeleteRoomMessage(MessageInterface):
    """Delete room message."""

    room_name: str
    
    @classmethod
    def from_bytes(cls, message_bytes: bytes) -> Self:
        """Create message from bytes."""
        message_dict = msgpack.loads(message_bytes) 
        return cls(room_name=message_dict["room_name"])

    def to_bytes(self: Self) ->bytes:
        """Serialize message to bytes."""
        return msgpack.dumps({"room_name": self.room_name})
