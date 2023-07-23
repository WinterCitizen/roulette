"""Module containing tests for server."""
import socket

from tornado.iostream import IOStream
from tornado.testing import bind_unused_port

from src.back.server import Server


async def test_server() -> None:
    """Test server echoes message."""
    # Given:
    sock, port = bind_unused_port()
    server = Server()
    server.add_socket(sock)

    client = IOStream(socket.socket())
    await client.connect(("localhost", port))

    message = b"HOLA\n"

    # When: Client writes a message to the socket
    await client.write(message)

    # Then: Server echoes the message
    assert await client.read_until(b"\n") == message
