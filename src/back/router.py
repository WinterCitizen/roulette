from typing import Self
from tornado.iostream import IOStream


class Router(MessageHandlerInterface):
    """"""

    def handle(self: Self, message: bytes, stream: IOStream) -> None:
        """"""
