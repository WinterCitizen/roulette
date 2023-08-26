"""Module containing tests for connection registry."""
from src.back.interfaces.values.connection import ConnectionRegistry
from tests.back.fake.io import FakeWriteStream


def test_store_connection() -> None:
    """Test connections are stored in connection registry."""
    # Given: two fake streams
    stream = FakeWriteStream()
    second_stream = FakeWriteStream()

    # When: we store stream in connection registry
    connection_registry = ConnectionRegistry()
    connection_registry.store_connection(stream)
    connection_registry.store_connection(second_stream)

    # Then: we check that streams are stored in connection registry
    connections = connection_registry.get_connections()

    assert connections == [stream, second_stream]


def test_close_connections() -> None:
    """Test connections are closed and we have no streams in connection registry."""
    # Given: a stream in connection registry
    stream = FakeWriteStream()
    connection_registry = ConnectionRegistry(connections=[stream])

    # When: we close each connection
    connection_registry.close_connection(stream)

    # Then: we check that connection is closed and we have no more connections in registry.
    connections = connection_registry.get_connections()

    assert not connections
