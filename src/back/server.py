"""TCP connection server."""
from typing import Any, Self

from tornado.iostream import IOStream
from tornado.tcpserver import TCPServer


class Server(TCPServer):
    """Tcp connection server."""

    async def handle_stream(self: Self, stream: IOStream, address: tuple[Any, ...]) -> None:
        """Ocerwritten handl_stream method."""
        while True:
            data = await stream.read_until(b"\n")
            await stream.write(data)
