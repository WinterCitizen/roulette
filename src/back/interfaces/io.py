"""Module containing the project IO interfaces."""
from collections.abc import Awaitable
from typing import Protocol, Self

from src.back.interfaces.message import MessageInterface


class MessagePrefixRegistryInterface(Protocol):
    """Registry storing message types & their prefixes."""

    def get_message_type(self: Self, prefix: int) -> type[MessageInterface]:
        """Get message type for the prefix."""
        raise NotImplementedError

    def get_prefix(self: Self, message_type: type[MessageInterface]) -> int:
        """Get prefix for the message type."""
        raise NotImplementedError


class ReadStreamInterface(Protocol):
    """An object reading bytes from the stream."""

    def read_until(
        self: Self,
        delimeter: bytes,
        max_bytes: int | None = None,
    ) -> Awaitable[bytes]:
        """Read bytes from the stream."""
        raise NotImplementedError


class WriteStreamInterface(Protocol):
    """An object writing bytes to the stream."""

    def write(self: Self, data: bytes | memoryview) -> Awaitable[None]:
        """Write bytes to the stream."""
        raise NotImplementedError
