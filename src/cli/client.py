"""TCP Client."""
from typing import Self

from tornado.tcpclient import TCPClient


class Client(TCPClient):
    """TCP Client."""

    msg_separator = b"\n"

    async def run(self: Self, host: str, port: int) -> bytes:
        """Run coroutine."""
        stream = await self.connect(host, port)
        while True:
            message = b"ping"
            message += self.msg_separator

            await stream.write(message)
            response = await stream.read_until(self.msg_separator)
            response.rstrip(self.msg_separator)
            return response
