from typing import Any, Self


from src.back.interfaces.message import MessageInterface
from src.back.interfaces.router import MessageHandlerInterface
from src.back.interfaces.io import WriteStreamInterface


class RoutingHandler(MessageHandlerInterface[MessageInterface]):
    """A message handler that routes incoming messages to appropriate handlers based on their type."""

    message_type_to_handlers: dict[ type[MessageInterface], tuple[MessageHandlerInterface[Any], ...]]

    def __init__(
        self: Self,
        message_type_to_handlers: dict[
            type[MessageInterface],
            tuple[MessageHandlerInterface[Any], ...],
        ],
    ) -> None:
        self.message_type_to_handlers = message_type_to_handlers

    async def handle( self: Self, message: MessageInterface, stream: WriteStreamInterface) -> None:
        """Process the incoming message."""
        handlers = self.message_type_to_handlers.get(type(message), ())

        for handler in handlers:
            await handler.handle(message, stream)
