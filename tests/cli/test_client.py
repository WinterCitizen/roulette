"""Module containing tests for client."""
from tornado.testing import bind_unused_port

from src.back.server import Server
from src.cli.client import Client


async def test_client() -> None:
    """Test client response."""
    # Given:
    sock, port = bind_unused_port()
    server = Server()
    server.add_socket(sock)

    client = Client()

    # When: client is sending a message to server
    response = await client.run("localhost", port)

    # Then: Client responses with a message
    assert response == b"ping\n"
