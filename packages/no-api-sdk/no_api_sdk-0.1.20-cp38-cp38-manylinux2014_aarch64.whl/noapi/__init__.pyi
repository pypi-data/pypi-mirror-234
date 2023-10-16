from .await_async import *
from .datanet import *
from .datatypes import *
from .Item import *
from .List import *
from .Link import *
from .msg import *
from .Property import *
from .Slice import *
import asyncio
import logging
from .Item import Item
from .Link import Link as Link
from .List import List as List
from .Property import Property as Property
from _typeshed import Incomplete
from logging import INFO
from typing import Any, Optional, Tuple
from typing_extensions import TypeAlias

upython: bool
NOTICE = INFO
console = logging
NUMBER: str
STRING: str
BOOLEAN: str
DATE: str
PropertyValue: TypeAlias
Field: TypeAlias
GetResult: TypeAlias

class WebSocketAsWebSocket:
    def __init__(self, socket: Any) -> None: ...
    async def send(self, data: str) -> None: ...
    async def recv(self) -> str: ...
    async def close(self) -> None: ...

class TcpSocketAsWebSocket(WebSocketAsWebSocket):
    def __init__(self, socket: Tuple[asyncio.StreamReader, Any]) -> None: ...
    async def send(self, data: str) -> None: ...
    async def recv(self) -> str: ...
    async def close(self) -> None: ...

class noapi:
    features: Incomplete
    first_response: Incomplete
    well_known_propids: Incomplete
    websocket: Incomplete
    websocket_url: Incomplete
    tcp_host: Incomplete
    tcp_port: int
    def __init__(self, socket_url: Optional[str] = ...) -> None: ...
    @staticmethod
    def client_version(self: Incomplete | None = ...) -> str: ...
    @staticmethod
    def server_version(self: Incomplete | None = ...) -> Optional[str]: ...
    @staticmethod
    def set_websocket(ws_url: str) -> None: ...
    def datastore(self, datastore_url: Optional[str] = ...) -> Item: ...
    @staticmethod
    def run(cls, mainf: Any = ...) -> Any: ...

def run(mainf: Any) -> Any: ...
def datastore(datastore_url: str) -> Item: ...
def client_version() -> str: ...
def server_version() -> Optional[str]: ...
def set_websocket(ws_url: str) -> None: ...
def disconnect() -> None: ...
