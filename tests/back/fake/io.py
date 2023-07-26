"""Module containing fake stream implementation."""
from typing import Self

from src.back.interfaces.io import WriteStreamInterface


class FakeWriteStream(WriteStreamInterface):
    """Fake write stream implementation storing written data."""

    write_bytes: bytes

    async def write(self: Self, data: bytes | memoryview) -> None:
        """Write given data to the local buffer."""
        if isinstance(data, memoryview):
            msg = "Memoryview is not supported"
            raise TypeError(msg)

        self.write_bytes = data
