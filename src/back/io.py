"""Module containing the project IO abstractions."""
import dataclasses
from types import MappingProxyType
from typing import Self

from src.back.interfaces.io import (
    MessagePrefixRegistryInterface,
    ReadStreamInterface,
    WriteStreamInterface,
)
from src.back.interfaces.message import MessageInterface


@dataclasses.dataclass
class IOConfig:
    """Message configuration."""

    max_message_size: int
    message_prefix_size: int
    message_length_size: int


class MessagePrefixRegistry(MessagePrefixRegistryInterface):
    """Registry storing messages & their prefixes."""

    _prefix_to_message_type: MappingProxyType[int, type[MessageInterface]]
    _message_type_to_prefix: MappingProxyType[type[MessageInterface], int]

    def __init__(
        self: Self,
        prefix_to_message_type: dict[int, type[MessageInterface]],
    ) -> None:
        """Construct the message prefix registry."""
        if len(set(prefix_to_message_type.values())) != len(prefix_to_message_type):
            msg = "Message can't be associated to multiple types"
            raise ValueError(msg)

        self._prefix_to_message_type = MappingProxyType(prefix_to_message_type)
        self._message_type_to_prefix = MappingProxyType(
            {value: key for key, value in prefix_to_message_type.items()},
        )

    def get_message_type(self: Self, prefix: int) -> type[MessageInterface]:
        """Get message type for prefix."""
        message_type = self._prefix_to_message_type.get(prefix)
        if message_type is None:
            msg = f"There is no message type for prefix {prefix}"
            raise ValueError(msg)

        return message_type

    def get_prefix(self: Self, message_type: type[MessageInterface]) -> int:
        """Get prefix for the message type."""
        prefix = self._message_type_to_prefix.get(message_type)

        if prefix is None:
            msg = f"There is no prefix for message type {message_type}"
            raise ValueError(msg)

        return prefix


@dataclasses.dataclass
class MessageReader:
    """An object reading messages from the stream."""

    message_prefix_registry: MessagePrefixRegistry
    config: IOConfig

    async def read(self: Self, read_stream: ReadStreamInterface) -> MessageInterface:
        """Read the message from the stream."""
        prefix_bytes = await read_stream.read_bytes(self.config.message_prefix_size)
        prefix = int.from_bytes(prefix_bytes, "big")
        length_bytes = await read_stream.read_bytes(self.config.message_length_size)
        content_length = int.from_bytes(length_bytes, "big")

        if content_length > self.config.max_message_size:
            msg = f"Cannot process large messages. MAX: {self.config.max_message_size}. GIVEN: {content_length}"
            raise ValueError(msg)

        message_bytes = await read_stream.read_bytes(content_length)
        message_type = self.message_prefix_registry.get_message_type(prefix)

        return message_type.from_bytes(message_bytes)


@dataclasses.dataclass
class MessageWriter:
    """An object writing messages into the stream."""

    message_prefix_registry: MessagePrefixRegistry
    config: IOConfig

    async def write(
        self: Self,
        write_stream: WriteStreamInterface,
        message: MessageInterface,
    ) -> None:
        """Write the message to the stream."""
        prefix = self.message_prefix_registry.get_prefix(type(message))

        message_bytes = message.to_bytes()
        if len(message_bytes) > self.config.max_message_size:
            msg = f"Cannot process large messages. MAX: {self.config.max_message_size}. GIVEN: {len(message_bytes)}"
            raise ValueError(msg)

        content_length = len(message_bytes).to_bytes(4, "big")
        await write_stream.write(prefix.to_bytes(2, "big") + content_length + message_bytes)
