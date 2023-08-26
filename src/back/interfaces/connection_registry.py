"""Module containing interface for connections."""
from typing import Protocol, Self

from src.back.interfaces.io import WriteStreamInterface


class ConnectionRegistryInterface(Protocol):
    """Interface for connections storage."""

    def store_connection(self: Self, stream: WriteStreamInterface) -> None:
        """Store stream to storage."""
        raise NotImplementedError

    def close_connection(self: Self, stream: WriteStreamInterface) -> None:
        """Close connection and remove stream from storage."""
        raise NotImplementedError

    def get_connections(self: Self) -> list[WriteStreamInterface]:
        """Return list of connections."""
        raise NotImplementedError
