from typing import Self, Protocol
from tornado.iostream import IOStream


class MessageHandlerInterface(Protocol):
    """Interface for handling messages in the router."""

    def handle(self: Self, message: bytes, stream: IOStream) -> None:
        """Process the incoming message."""
        raise NotImplementedError
