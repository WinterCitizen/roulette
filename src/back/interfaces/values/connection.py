"""Module containing implementation of stream storage."""
import dataclasses
from typing import Self

from src.back.interfaces.connection_registry import ConnectionRegistryInterface
from src.back.interfaces.io import WriteStreamInterface


@dataclasses.dataclass
class ConnectionRegistry(ConnectionRegistryInterface):
    """Interface for connections storage."""

    connections: list[WriteStreamInterface] = dataclasses.field(
        default_factory=list,
    )

    def store_connection(self: Self, stream: WriteStreamInterface) -> None:
        """Store stream to storage."""
        self.connections.append(stream)

    def close_connection(self: Self, stream: WriteStreamInterface) -> None:
        """Close connection and remove stream from storage."""
        ind = self.connections.index(stream)
        stream.close()
        self.connections.pop(ind)

    def get_connections(self: Self) -> list[WriteStreamInterface]:
        """Return list of connections."""
        return self.connections
