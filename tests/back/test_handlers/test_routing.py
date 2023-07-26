"""Module testing routing handler."""
from typing import Self

import pytest

from src.back.handlers.routing import RoutingHandler
from src.back.interfaces.handlers import MessageHandlerInterface
from src.back.interfaces.io import WriteStreamInterface
from tests.back.fake.io import FakeWriteStream
from tests.back.test_io import FakeMessage


class FakeMessageHandler(MessageHandlerInterface[FakeMessage]):
    """Fake message handler implementation."""

    handled: bool = False

    async def handle(
        self: Self,
        message: FakeMessage,
        stream: WriteStreamInterface,
    ) -> None:
        """Mark message handler as handled."""
        self.handled = True


async def test_routing_handler() -> None:
    """Test that routing handler routes messages."""
    # Given: routing handler with registered handler for fake message
    fake_handler = FakeMessageHandler()

    routing_handler = RoutingHandler(
        message_type_to_handlers={
            FakeMessage: (fake_handler,),
        },
    )

    # When: routing handler's handle method is called with fake message
    await routing_handler.handle(FakeMessage(message="test"), FakeWriteStream())

    # Then: handler registered for the fake message is called
    assert fake_handler.handled


async def test_empty_routing_handler() -> None:
    """Test routing handler's handling of unregistered messages."""
    # Given: routing handler with no routes registered
    routing_handler = RoutingHandler(message_type_to_handlers={})

    # When: message is passed to routing handler's handle method
    # Then: an error is raised
    with pytest.raises(TypeError, match="There is no handlers for message with type"):
        await routing_handler.handle(FakeMessage(message="test"), FakeWriteStream())
