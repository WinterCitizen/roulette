"""Module testing backend's main."""
from typing import Self

from src.back.main import main


class FakeServer:
    """Fake listenable server implementation."""

    listening: bool = False

    def listen(self: Self, port: int) -> None:
        """Set server state to listening."""
        self.listening = True


class FakeEvent:
    """Fake waitable event implementation."""

    waiting: bool = False

    async def wait(self: Self) -> None:
        """Set event state to waiting."""
        self.waiting = True


async def test_main() -> None:
    """Test that backend main is working."""
    # Given:
    fake_server = FakeServer()
    fake_event = FakeEvent()

    # When: main function is called
    await main(server=fake_server, port=8000, event=fake_event)

    # Then: the server is listening & event is waiting
    assert fake_server.listening
    assert fake_event.waiting
