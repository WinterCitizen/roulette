"""Module containing project's application container."""
import asyncio

from dependency_injector import containers, providers
from tornado.iostream import IOStream
from tornado.tcpclient import TCPClient

from src.back.handlers.create_room import CreateRoomHandler
from src.back.handlers.join_room import JoinRoomHandler
from src.back.handlers.ping import PingHandler
from src.back.handlers.routing import RoutingHandler
from src.back.interfaces.values.connection import ConnectionRegistry
from src.back.io import IOConfig, MessagePrefixRegistry, MessageReader, MessageWriter
from src.back.message.create_room import CreateRoomMessage
from src.back.message.join_room import JoinRoomMessage
from src.back.message.ping import PingMessage, PongMessage
from src.back.notifier.notifier import Notification
from src.back.room_registry import RoomRegistry
from src.back.server import Server
from src.cli.client import Client


async def init_client_stream(host: str, port: int) -> IOStream:
    """Create stream for the given host/port."""
    return await TCPClient().connect(host, port)


class ApplicationContainer(containers.DeclarativeContainer):
    """Root container for the project dependencies."""

    config = providers.Configuration()
    io_config = providers.Factory(
        IOConfig,
        max_message_size=config.MAX_MESSAGE_SIZE,
        message_prefix_size=config.MESSAGE_PREFIX_SIZE,
        message_length_size=config.MESSAGE_LENGTH_SIZE,
    )
    message_prefix_registry = providers.Factory(
        MessagePrefixRegistry,
        providers.Dict(
            {
                1: PingMessage,
                2: PongMessage,
                3: CreateRoomMessage,
                4: JoinRoomMessage,
            },
        ),
    )

    message_reader = providers.Factory(
        MessageReader,
        message_prefix_registry=message_prefix_registry,
        config=io_config,
    )
    message_writer = providers.Factory(
        MessageWriter,
        message_prefix_registry=message_prefix_registry,
        config=io_config,
    )

    room_registry = providers.Singleton(RoomRegistry, rooms_lock=asyncio.Lock())

    connection_registry = providers.Singleton(
        ConnectionRegistry,
    )

    notification = providers.Singleton(
        Notification,
        room_registry=room_registry,
        connection_registry=connection_registry,
    )

    ping_handler = providers.Factory(PingHandler, message_writer=message_writer, notifier=notification)

    create_room_handler = providers.Factory(
        CreateRoomHandler,
        room_registry=room_registry,
        notifier=notification,
    )

    join_room_handler = providers.Factory(
        JoinRoomHandler,
        room_registry=room_registry,
        notifier=notification,
    )

    routing_handler = providers.Factory(
        RoutingHandler,
        message_type_to_handlers=providers.Dict(
            {
                PingMessage: providers.List(ping_handler),
                CreateRoomMessage: providers.List(create_room_handler),
                JoinRoomMessage: providers.List(join_room_handler),
            },
        ),
    )

    server = providers.Factory(
        Server,
        message_reader=message_reader,
        message_writer=message_writer,
        message_handler=routing_handler,
        connection_registry=connection_registry,
    )
    event = providers.Factory(asyncio.Event)

    client_stream = providers.Resource(
        init_client_stream,
        host=config.HOST,
        port=config.PORT,
    )
    client = providers.Singleton(
        Client,
        stream=client_stream,
        message_reader=message_reader,
        message_writer=message_writer,
    )
