"""Module containing ping message handler."""
import dataclasses
from typing import Self

from src.back.interfaces.handlers import MessageHandlerInterface
from src.back.interfaces.io import WriteStreamInterface
from src.back.io import MessageWriter
from src.back.message.ping import PingMessage, PongMessage


@dataclasses.dataclass
class PingHandler(MessageHandlerInterface[PingMessage]):
    """Ping handler."""

    message_writer: MessageWriter

    async def handle(
        self: Self,
        message: PingMessage,
        stream: WriteStreamInterface,
    ) -> None:
        """Response with pong on any ping."""
        await self.message_writer.write(stream, PongMessage())
