"""Module testing the project io."""
import dataclasses
from typing import Self, TypeVar

import msgpack
import pytest

from src.back.interfaces.io import ReadStreamInterface
from src.back.interfaces.message import MessageInterface
from src.back.io import MessagePrefixRegistry, MessageReader, MessageWriter
from tests.back.fake.io import FakeWriteStream

T = TypeVar("T")


@dataclasses.dataclass
class FakeMessage(MessageInterface):
    """Fake message used for testing."""

    message: str

    @classmethod
    def from_bytes(cls, message_bytes: bytes) -> Self:
        """Create fake message from bytes."""
        message_dict = msgpack.loads(message_bytes)

        return cls(message=message_dict["message"])

    def to_bytes(self: Self) -> bytes:
        """Serialize message to bytes."""
        return msgpack.dumps({"message": self.message})


@dataclasses.dataclass
class FakeReadStream(ReadStreamInterface):
    """Fake read stream implementation reading the hardcoded data."""

    read_bytes: bytes

    async def read_until(
        self: Self,
        delimeter: bytes,
        max_bytes: int | None = None,
    ) -> bytes:
        """Read hardcoded data ignoring the delimiter & max_bytes."""
        return self.read_bytes


async def test_message_reader_writer() -> None:
    """Test that message reader/writer work."""
    # Given: message prefix registry with message type registered
    message_prefix_registry = MessagePrefixRegistry(
        prefix_to_message_type={1: FakeMessage},
    )
    message_reader = MessageReader(message_prefix_registry=message_prefix_registry)
    message_writer = MessageWriter(message_prefix_registry=message_prefix_registry)

    write_stream = FakeWriteStream()
    original_message = FakeMessage(message="test")

    # When: registered message is passed to writer's write method
    # Then: the message is written to the writer
    await message_writer.write(write_stream=write_stream, message=original_message)

    read_stream = FakeReadStream(read_bytes=write_stream.write_bytes)

    # When: bytes serialized by the writer are used to read the message in reader
    message = await message_reader.read(read_stream=read_stream)

    # Then: originally written message is returned
    assert isinstance(message, FakeMessage)
    assert message == original_message


def test_message_prefix_registry_validation() -> None:
    """Test that message prefix registry can't be instantiated with same values for multiple prefixes."""
    # Given:
    # When: message prefix registry is instantiated with the same message types for multiple prefixes
    # Then: an error is raised
    with pytest.raises(
        ValueError,
        match="Message can't be associated to multiple types",
    ):
        MessagePrefixRegistry(prefix_to_message_type={1: FakeMessage, 2: FakeMessage})


def test_message_registry_get_message_type() -> None:
    """Test that get message type raises an error on empty registry."""
    # Given: empty prefix registry
    message_prefix_registry = MessagePrefixRegistry(prefix_to_message_type={})

    # When: get message type method is called for any prefix
    # Then: an error is raised
    with pytest.raises(ValueError, match="There is no message type for prefix"):
        message_prefix_registry.get_message_type(1)


def test_message_registry_get_prefix() -> None:
    """Test that get prefix raises an error on empty registry."""
    # Given: empty prefix registry
    message_prefix_registry = MessagePrefixRegistry(prefix_to_message_type={})

    # When: get prefix method is called for any message type
    # Then: an error is raised
    with pytest.raises(ValueError, match="There is no prefix for message type"):
        message_prefix_registry.get_prefix(FakeMessage)
