"""Main module instantiating client."""
import asyncio

from src.cli.client import Client
from src.settings.settings import Settings


async def main(host: str, port: int) -> None:
    """Connect to server."""
    client = Client()
    asyncio.run(client.run(host, port))

if __name__ == "__main__":
    settings = Settings()
    asyncio.run(main(settings.HOST, settings.PORT))
