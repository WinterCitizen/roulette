"""Main module instantiating server."""
from typing import Protocol, Self

from dependency_injector.wiring import Provide, inject

from src.back.containers.application import ApplicationContainer


class ServerInterface(Protocol):
    """Listenable server interface."""

    def listen(self: Self, port: int) -> None:
        """Listen on the given port."""
        raise NotImplementedError


class EventInterface(Protocol):
    """Waitable event interface."""

    async def wait(self: Self) -> None:
        """Wait for event."""
        raise NotImplementedError


@inject
async def main(
    server: ServerInterface = Provide[ApplicationContainer.server],
    port: int = Provide[ApplicationContainer.config.PORT],
    event: EventInterface = Provide[ApplicationContainer.event],
) -> None:
    """Start the server."""
    server.listen(port)
    await event.wait()
