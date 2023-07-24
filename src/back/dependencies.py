"""Module containing project dependencies."""
from src.back.containers.application import ApplicationContainer
from src.settings.settings import Settings

APPLICATION_DEPENDENCIES = ApplicationContainer()


def wire_dependencies() -> None:
    """Wire dependencies to requred modules."""
    APPLICATION_DEPENDENCIES.config.from_dict(Settings().__dict__)  # type: ignore[call-arg]

    APPLICATION_DEPENDENCIES.wire(
        (
            "src.back.main",
        ),
    )
