"""Module containing which serves as an interface for handling messages in the router."""
from typing import Protocol, Self

from src.back.interfaces.io import WriteStreamInterface
from src.back.interfaces.message import MessageInterface


class MessageHandlerInterface(Protocol):
    """Interface for handling messages in the router."""

    async def handle( self: Self, message: MessageInterface, stream: WriteStreamInterface) -> None:
        """Process the incoming message."""
        raise NotImplementedError
