"""Package containing ping message."""
import dataclasses
from typing import Self

from src.back.interfaces.message import MessageInterface


@dataclasses.dataclass
class PingMessage(MessageInterface):
    """Ping message."""

    @classmethod
    def from_bytes(cls, message_bytes: bytes) -> Self:
        """Create ping message from bytes."""
        return cls()

    def to_bytes(self: Self) -> bytes:
        """Serialize ping message to bytes."""
        return b""


@dataclasses.dataclass
class PongMessage(MessageInterface):
    """Pong message."""

    @classmethod
    def from_bytes(cls, message_bytes: bytes) -> Self:
        """Create pong message from bytes."""
        return cls()

    def to_bytes(self: Self) -> bytes:
        """Serialize pong message to bytes."""
        return b""
