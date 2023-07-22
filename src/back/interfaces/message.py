"""Module with the message interface."""
from typing import Protocol, Self


class MessageInterface(Protocol):
    """Interface for all messages going in/out of the server."""

    @classmethod
    def from_bytes(cls, message_bytes: bytes) -> Self:
        """Create the message from bytes."""
        raise NotImplementedError

    def to_bytes(self: Self) -> bytes:
        """Serialize message to bytes."""
        raise NotImplementedError
