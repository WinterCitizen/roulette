"""TCP connection server."""
from typing import Any, Self

from tornado.iostream import IOStream
from tornado.tcpserver import TCPServer

from src.back.io import MessageReader, MessageWriter
from src.back.message.ping import PingMessage, PongMessage


class Server(TCPServer):
    """Tcp connection server."""

    message_reader: MessageReader
    message_writer: MessageWriter

    def __init__(
        self: Self,
        message_reader: MessageReader,
        message_writer: MessageWriter,
        *args: Any,
        **kwargs: Any,
    ) -> None:
        """Init the server."""
        self.message_reader = message_reader
        self.message_writer = message_writer

        super().__init__(*args, **kwargs)

    async def handle_stream(self: Self, stream: IOStream, address: tuple[Any, ...]) -> None:
        """Ocerwritten handl_stream method."""
        while True:
            message = await self.message_reader.read(stream)

            if isinstance(message, PingMessage):
                await self.message_writer.write(stream, PongMessage())
