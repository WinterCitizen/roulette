"""Module containing routing message handler."""
import dataclasses
from asyncio import gather
from collections.abc import Sequence
from typing import Any, Self

from src.back.interfaces.handlers import MessageHandlerInterface
from src.back.interfaces.io import WriteStreamInterface
from src.back.interfaces.message import MessageInterface


@dataclasses.dataclass
class RoutingHandler(MessageHandlerInterface[MessageInterface]):
    """Handler routing messages to corresponding message handlers."""

    message_type_to_handlers: dict[type[MessageInterface], Sequence[MessageHandlerInterface[Any]]]

    async def handle(
        self: Self,
        message: MessageInterface,
        stream: WriteStreamInterface,
    ) -> None:
        """Route message to it's corresponding message handlers."""
        message_handlers = self.message_type_to_handlers.get(type(message), ())

        if not message_handlers:
            msg = f"There is no handlers for message with type {type(message)}"
            raise TypeError(msg)

        await gather(
            *(message_handler.handle(message, stream) for message_handler in message_handlers),
        )
