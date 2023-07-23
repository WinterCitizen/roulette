"""Main module instantiating server."""
import asyncio

from src.back.server import Server
from src.settings.settings import Settings


async def main(port: int) -> None:
    """Listen to server."""
    server = Server()
    server.listen(port)
    await asyncio.Event().wait()


if __name__ == "__main__":
    settings = Settings()
    asyncio.run(main(settings.PORT))
