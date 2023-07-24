"""Module containing project's application container."""
import asyncio

from dependency_injector import containers, providers
from tornado.iostream import IOStream
from tornado.tcpclient import TCPClient

from src.back.io import MessagePrefixRegistry, MessageReader, MessageWriter
from src.back.message.ping import PingMessage, PongMessage
from src.back.server import Server
from src.cli.client import Client


async def init_client_stream(host: str, port: int) -> IOStream:
    """Create stream for the given host/port."""
    return await TCPClient().connect(host, port)

class ApplicationContainer(containers.DeclarativeContainer):
    """Root container for the project dependencies."""

    config = providers.Configuration()

    message_prefix_registry = providers.Factory(
        MessagePrefixRegistry,
        providers.Dict(
            {
                1: PingMessage,
                2: PongMessage,
            },
        ),
    )

    message_reader = providers.Factory(MessageReader, message_prefix_registry=message_prefix_registry)
    message_writer = providers.Factory(MessageWriter, message_prefix_registry=message_prefix_registry)

    server = providers.Factory(Server, message_reader=message_reader, message_writer=message_writer)
    event = providers.Factory(asyncio.Event)

    client_stream = providers.Resource(init_client_stream, host=config.HOST, port=config.PORT)
    client = providers.Singleton(
        Client,
        stream=client_stream,
        message_reader=message_reader,
        message_writer=message_writer,
    )
