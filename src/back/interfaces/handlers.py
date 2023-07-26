"""Module containing handlers' interfaces."""
from typing import Protocol, Self, TypeVar

from src.back.interfaces.io import WriteStreamInterface
from src.back.interfaces.message import MessageInterface

T_contra = TypeVar("T_contra", bound=MessageInterface, contravariant=True)


class MessageHandlerInterface(Protocol[T_contra]):
    """Message handler interface."""

    async def handle(
        self: Self,
        message: T_contra,
        stream: WriteStreamInterface,
    ) -> None:
        """Handle message."""
        raise NotImplementedError
