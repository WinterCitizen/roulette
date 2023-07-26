"""TCP connection server."""
from asyncio import Task
from typing import Any, Self

from tornado.iostream import IOStream
from tornado.tcpserver import TCPServer

from src.back.interfaces.handlers import MessageHandlerInterface
from src.back.interfaces.message import MessageInterface
from src.back.io import MessageReader, MessageWriter


class Server(TCPServer):
    """Tcp connection server."""

    message_reader: MessageReader
    message_writer: MessageWriter
    message_handler: MessageHandlerInterface[MessageInterface]

    def __init__(
        self: Self,
        message_reader: MessageReader,
        message_writer: MessageWriter,
        message_handler: MessageHandlerInterface[MessageInterface],
        *args: Any,
        **kwargs: Any,
    ) -> None:
        """Init the server."""
        self.message_reader = message_reader
        self.message_writer = message_writer
        self.message_handler = message_handler

        super().__init__(*args, **kwargs)

    async def handle_stream(
        self: Self,
        stream: IOStream,
        address: tuple[Any, ...],
    ) -> None:
        """Ocerwritten handl_stream method."""
        while True:
            message = await self.message_reader.read(stream)

            Task(self.message_handler.handle(message, stream))
