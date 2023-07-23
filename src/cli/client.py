"""TCP Client."""
from __future__ import annotations

import dataclasses
from typing import TYPE_CHECKING, Self

from src.back.interfaces.io import ReadStreamInterface, WriteStreamInterface

if TYPE_CHECKING:
    from src.back.interfaces.message import MessageInterface
    from src.back.io import MessageReader, MessageWriter



class ReadWriteStreamInterface(ReadStreamInterface, WriteStreamInterface):
    """Read/Write stream interface."""


@dataclasses.dataclass
class Client:
    """Client capable of reading/writing messages through the stream."""

    stream: ReadWriteStreamInterface
    message_reader: MessageReader
    message_writer: MessageWriter

    async def read(self: Self) -> MessageInterface:
        """Read message from the stream."""
        return await self.message_reader.read(self.stream)

    async def write(self: Self, message: MessageInterface) -> None:
        """Write message to the stream."""
        await self.message_writer.write(self.stream, message)
