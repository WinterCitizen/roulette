"""Module running the tcp server."""
import asyncio

from src.back.dependencies import wire_dependencies
from src.back.main import main

if __name__ == "__main__":
    wire_dependencies()

    asyncio.run(main())
