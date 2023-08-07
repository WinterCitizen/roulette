"""Module containing user implementation."""
import dataclasses
from typing import Self


@dataclasses.dataclass
class User:
    """User implementation."""

    name: str

    def as_dict(self: Self) -> dict[str, str]:
        """Convert object to dict."""
        return {
            "name": self.name,
        }
