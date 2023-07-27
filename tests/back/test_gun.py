"""Module containing tests for gun."""
from src.back.gun import Gun


def test_gun_shuffle() -> None:
    """Test gun shuffles clip."""
    # Given:
    gun = Gun(slots=5)
    clip = gun.get_clip().copy()

    # When: we shuffle gun
    gun.shuffle(seed=1)

    # Then: we check that clip was shuffled
    shuffled_clip = gun.get_clip()
    assert clip != shuffled_clip


def test_gun_fire() -> None:
    """Test gun fire clip."""
    # Given:
    gun = Gun(slots=5)

    # When: we fire gun with dummy bullet
    gun.shuffle(seed=1)
    fired = gun.fire()

    # Then: we check that gun was fired with dummy bullet
    assert fired is False

    # When: we fire gun with real bullet
    gun.shuffle(seed=6)
    fired = gun.fire()

    # Then: we check that gun was fired with real bullet
    assert fired is True
