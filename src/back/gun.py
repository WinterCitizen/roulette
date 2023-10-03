"""Module containing gun implementation."""
import random
from random import shuffle
from typing import Self

from src.back.interfaces.gun import GunInterface


class Gun(GunInterface):
    """Interface for gun."""

    def __init__(self: Self, slots: int = 6) -> None:
        """Construct gun with clip size and a bullet."""
        self.slots = slots
        self.clip = self._fill_clip(slots)

    def shuffle(self: Self, seed: int | None = None) -> None:
        """Shuffle gun clip.

        :param seed: int, Needed for tests.
        """
        random.seed(seed)

        shuffle(self.clip)

    def fire(self: Self) -> bool:
        """Fire bullet."""
        return self.clip[0] == 1

    def get_clip(self: Self) -> list[int]:
        """Get clip."""
        return self.clip

    def _fill_clip(self: Self, slots: int) -> list[int]:
        """Fill clip with a bullet."""
        clip = [1]
        clip.extend([0 for _ in range(slots - 1)])
        return clip
