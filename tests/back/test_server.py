"""Module containing tests for server."""

from tornado.testing import bind_unused_port

from src.back.dependencies import APPLICATION_DEPENDENCIES
from src.back.message.ping import PingMessage, PongMessage


async def test_server() -> None:
    """Test server echoes message."""
    # Given:
    server = APPLICATION_DEPENDENCIES.server()

    sock, port = bind_unused_port()
    server.add_socket(sock)

    with APPLICATION_DEPENDENCIES.config.PORT.override(port):
        client = await APPLICATION_DEPENDENCIES.client()  # type: ignore[misc]

    # When: Client writes a message to the socket
    await client.write(PingMessage())

    # Then: Server echoes the message
    assert await client.read() == PongMessage()
