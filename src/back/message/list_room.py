import dataclasses
from typing import Self

import msgpack

from src.back.interfaces.message import MessageInterface


@dataclasses.dataclass
class ListRoomsMessage(MessageInterface):
    @classmethod
    def from_bytes(cls, message_bytes: bytes) -> Self:
        """Create message from bytes."""
        return cls()

    def to_bytes(self: Self) -> bytes:
        """Serialize message to bytes."""
        return msgpack.dumps({})
