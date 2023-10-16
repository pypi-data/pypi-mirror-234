# emacs mycoding: utf-8
# mypy: disallow-untyped-defs
# mypy: check-untyped-defs
# mypy: disallow-incomplete-defs

from ._version import __version__

if __version__.startswith("git"):
    print("typeguard active")
    from typeguard import install_import_hook
    install_import_hook([".await_async",".datanet",".datatypes",".Item",".Link",".List",".msg",".Property",".Slice"])
    from .await_async import *
    from .datanet import *
    from .datatypes import *
    from .Item import *
    from .List import *
    from .Link import *
    from .List import *
    from .msg import *
    from .Property import *
    from .Slice import *

# patch to allow neste event loops
# import nest_asyncio  # type: ignore
# nest_asyncio.apply()
# import inspect

import asyncio
from .await_async import _await_async
from .msg import msg
import sys, errno
import os
import random


upython = False
if sys.implementation.name == "micropython":
    upython = True

# from decimal import Decimal
# from functools import partial
from .datanet import _datanet_args, _datanet_encode, _datanet_decode, _datanet_args_decode, _datanet_args_encode
from .Item import Item
import logging
from typing import Any, Optional, Tuple, Dict, Union, Any, TYPE_CHECKING
from typing_extensions import TypeAlias
import typing
from logging import DEBUG, INFO # except WARNING, ERROR, CRITICAL which require python classes
NOTICE=INFO # since python does not have a NOTICE level, we use INFO instead
from .Link import Link
from .List import List
from .Property import Property

console = logging

# datatypes (to be used as noapi.str)
NUMBER = "num"
STRING = "str"
BOOLEAN = "bol"
DATE = "dat"

PropertyValue: TypeAlias = Union[str, bool, int, float, None]  # TODO: add date field
Field: TypeAlias = Union["Property", "Link", "List", "Item", None]
GetResult: TypeAlias = Union[
    PropertyValue, "Item", "List", None
]  # PropValue instead of Prop and Item instead of Link

from websockets.exceptions import ConnectionClosedOK, ConnectionClosedError

class WebSocketAsWebSocket:
    def __init__(
        self, socket: Any
    ) -> None:  # Any could be StreamReader,StreamWriter, but write vs. awrite below is an issue
        self._socket = socket

    async def send(self, data: str) -> None:  # FIXME: data is binary maybe?
        try:
            return await self._socket.send(data)
        except ConnectionClosedError:
            # TODO: try to reconnect and resend?
            raise
        except Exception as e:
            raise

    async def recv(self) -> str:  # FIXME: binary maybe?
        try:
            return await self._socket.recv()
        except (ConnectionError, ConnectionClosedOK):
            raise # FIXME: should try to reconnect and resend

    async def close(self) -> None:
        if self._socket is not None:
            await self._socket.close()


class TcpSocketAsWebSocket(WebSocketAsWebSocket):
    def __init__(
        self, socket: Tuple[asyncio.StreamReader, Any]
    ) -> None:  # Any could be StreamReader,StreamWriter, but write vs. awrite below is an issue
        self._socket = socket
        self._reader = socket[0]
        self._writer = socket[1]

    async def send(self, data: str) -> None:  # FIXME: data is binary maybe?
        length = ">------<"  # FIXME: calculate a real length
        data = length + data
        if hasattr(self._writer, "write"):
            self._writer.write(data.encode())
            await self._writer.drain()
        else:
            await self._writer.awrite(data.encode())

    async def recv(self) -> str:  # FIXME: binary maybe?
        # length = await self._reader.read(8);
        length = 8191  # FIXME: get this from the first 8 bytes...
        data_read = await self._reader.read(8191)
        return data_read.decode("utf-8")  # FIXME: should deal with binary

    async def close(self) -> None:
        # self._reader.close()
        self._writer.close()
        # await self._reader.wait_closed()
        await self._writer.wait_closed()

class noapi:
    """
    noapi class
    """
    _noapi_instance = None

    def __init__(self, socket_url: Optional[str] = None) -> None:
        _noapi_instance = noapi._noapi_instance
        # print("Noapi:"+str(socket_url))
        # import traceback
        # traceback.print_stack()
        if noapi._noapi_instance is not None:
            if socket_url == _noapi_instance._socket_url_on_construct:
                self = _noapi_instance
                return
            else:
                raise Exception(
                    "Socket does not match:"
                    + str(_noapi_instance._socket_url_on_construct)
                    + " differs from "
                    + str(socket_url)
                )
        noapi._noapi_instance = self
        self._socket_url_on_construct: Optional[str] = socket_url
        if socket_url is None:
            if upython:
                socket_url = "tcp://default-wss.dev.no-api.net"
            else:
                socket_url = "wss://default-wss.dev.no-api.net/"
        self._localdb: Dict[str, Item] = {}
        self.features = ["exception_on_none_links"]
        self.__data_resolver: Dict[str, Any] = {}
        self._server_version_string: str = ""
        self.first_response = None
        self.__receive_loop: Optional[asyncio.Task] = None
        self.well_known_propids: Dict[str, str] = {}
        self.websocket: WebSocketAsWebSocket = WebSocketAsWebSocket(None)

        ws_added = False

        if socket_url[0:6] == "tcp://":
            self._proto = "tcp"
        elif socket_url[0:5] == "ws://":
            self._proto = "ws"
        elif socket_url[0:6] == "wss://":
            self._proto = "ws"
        else:
            socket_url = "wss://" + socket_url
            ws_added = True
            self._proto = "ws"

        if self._proto == "ws":
            wsurlparts = socket_url.split("/")
            hostport = wsurlparts[2]
            hostportparts = hostport.split(":")
            if len(hostportparts) < 2:
                # if there is no port, let's add a default port
                if (hostportparts[0] == "localhost") or (
                    hostportparts[0] == "127.0.0.1"
                ):
                    hostportparts.append("47080")
                    if ws_added:
                        wsurlparts[0] = "ws:"

            wsurlparts[2] = ":".join(hostportparts)
            self.websocket_url = "/".join(wsurlparts)
            # self.websocket_url = socket_url

        elif self._proto == "tcp":
            self.tcp_host = socket_url[6:]
            self.tcp_port = 47806  # 0xbabe, also ALC RFC5775
            if self.tcp_host.find(":") >= 0:
                self.tcp_port = int(self.tcp_host[self.tcp_host.find(":") + 1 :])
                self.tcp_host = socket_url[6 : self.tcp_host.find(":") + 6]

        else:
            raise Exception("url protocol unkonwn:" + self._proto)

    @staticmethod
    def client_version(self: "Optional[noapi]" = None) -> str:
        return("noapi-sdk-py."+str(__version__))

    @staticmethod
    def server_version(self: "Optional[noapi]" = None) -> Optional[str]:
        """
                implements :py:meth:`noapi_ref.Noapi.server_version`
        .. include: Makefile
        """


        if self:
            if hasattr(self, "_server_version_string"):
                return self._server_version_string
            else:
                return None


        if noapi._noapi_instance is None:
            return None

        return noapi._noapi_instance.server_version(noapi._noapi_instance)

    @staticmethod
    def set_websocket(ws_url: str) -> None:
        """implements :py:meth:`noapi_ref.Noapi.set_websocket`"""
        if noapi._noapi_instance is None:
            noapi._noapi_instance = noapi(ws_url)
        noapi._noapi_instance.set_websocket(ws_url)

    async def _async_disconnect(self, cancel_tasks: bool = False) -> None:
        receive_task = None
        nonsocket_tasks: typing.List[asyncio.Task] = []
        if self.__receive_loop is not None:
            asyncio.gather(self.__receive_loop)
        while len(nonsocket_tasks) > 0:
            alltasks = asyncio.all_tasks()
            nonsocket_tasks = []
            for task in alltasks:
                # task.get_coro comes in python, so we cant use it 3.8
                taskname = str(task)
                if (
                    ("async_disconnect" not in taskname)
                    and ("main" not in taskname)
                    and ("WebSocket" not in taskname)
                    and ("receive_loop" not in taskname)
                ):
                    nonsocket_tasks.append(task)
                if "receive_loop" in taskname:
                    receive_task = task
            # asyncio.gather(*nonsocket_tasks)
            # print("gathered non-socket tasks")

        _noapi_instance = noapi._noapi_instance
        if _noapi_instance is not None and _noapi_instance.websocket is not None:
            await _noapi_instance.websocket.close()
        if receive_task is not None:
            receive_task.cancel()
        if (
            self is not None
            and hasattr(self, "websocket")
            and self.websocket is not None
        ):
            await self.websocket.close()
        alltasks = asyncio.all_tasks()
        if cancel_tasks:
            for task in alltasks:
                taskname = str(task)
                if ("async_disconnect" not in taskname) and ("main" not in taskname):
                    print("Cancelling following task:")
                    print(taskname)
                    task.cancel()

    @classmethod
    def __get_a_future(cls: Any) -> Any: # FIXME: fix argument and return type
        if (hasattr(asyncio.get_event_loop(),"create_future")):
            return asyncio.get_event_loop().create_future()
        else: # micropython ??
            print("importing asyn")
            import asyn # type: ignore
            return asyn.Event() # type: ignore [attr-defined] #FIXME: test with micropython

    @staticmethod
    def _resolve_a_future(future,result): # type: ignore # FIXME: add types
        if (hasattr(future, "set_result")):
            future.set_result(result)
        else:
            future.set(result)
        return result

    def datastore(self, datastore_url: Optional[str] = None) -> Item: # when used as noapi().datastore(xx)
        tor = _await_async(self.__async_datastore(datastore_url))
        return tor

    async def __async_datastore(self, datastore_url: Optional[str] = None) -> Item:
        if datastore_url is None:
            # called statically as noapi.noapi.datastore() instead of noapi().datastore()
            if not isinstance(self, noapi):
                datastore_url = self
            else:
                raise Exception(
                    "datastore(datastore_url) call requires a datatstore_url parameter"
                )
            if noapi._noapi_instance is None:
                noapi._noapi_instance = noapi()
            return noapi._noapi_instance.datastore(datastore_url)

        _noapi_instance = noapi._noapi_instance
        if _noapi_instance is None:
            _noapi_instance = noapi()
        """
        implements :py:meth:`noapi_ref.noapi.datastore`
        """
        if _noapi_instance._proto == "ws":
            from websockets import client
            import websockets
            try:
                websocket = await client.connect(_noapi_instance.websocket_url,ping_timeout=None) # FIXME: maybe re-enable Timeout
                # _noapi_instance.websocket.websockets = websockets # FIXME: was this line needed?
            except websockets.exceptions.InvalidHandshake as e:
                msg._tell_dev(msg.M814_invalid_handshake__url, {"url": _noapi_instance.websocket_url})
            except OSError as e:
                myerrno = e.errno
                if myerrno is None:
                    if hasattr(e,"__context__") and hasattr(e.__context__,"errno"):
                        myerrno = e.__context__.errno
                if myerrno in [ errno.ECONNABORTED, errno.ECONNREFUSED, errno.ECONNRESET, errno.ENOTCONN, errno.ETIMEDOUT ]:
                    msg._tell_dev(msg.M815_oserr_connection_error__errno_url, {"errno": str(myerrno)+":"+os.strerror(myerrno), "url": _noapi_instance.websocket_url})
                else:
                    if repr(e) == "TimeoutError()":
                        msg._tell_dev(msg.M811_server_timeout__url, {"url": _noapi_instance.websocket_url})
                    else:
                        msg._tell_dev(msg.M711_unexpected_exception__exception, {"exception": repr(e)})
            except ConnectionError as e:
                msg._tell_dev(msg.M813_connection_error__url, {"url":_noapi_instance.websocket_url})
            except websockets.exceptions.InvalidURI as e:
                msg._tell_dev(msg.M812_server_invalid_url__url, {"url": _noapi_instance.websocket_url})
            except asyncio.TimeoutError:
                msg._tell_dev(msg.M811_server_timeout__url, {"url": _noapi_instance.websocket_url})
            except Exception as e:
                msg._tell_dev(msg.M711_unexpected_exception__exception, {"exception": str(e)})

            _noapi_instance.websocket = WebSocketAsWebSocket(websocket)
        elif _noapi_instance._proto == "tcp":
            # print("connection to "+_noapi_instance.tcp_host+" port "+str(_noapi_instance.tcp_port))
            try:
                tcpsocket = await asyncio.open_connection(
                    _noapi_instance.tcp_host, _noapi_instance.tcp_port
                )
            except ConnectionRefusedError as e:
                msg._tell_dev(msg.M813_connection_error__url, {"url": _noapi_instance.tcp_host+":"+str(_noapi_instance.tcp_port)})
            except OSError as e:
                myerrno = e.errno
                if myerrno is None:
                    myerrno = e.__context__.errno
                if myerrno in [ errno.ECONNABORTED, errno.ECONNREFUSED, errno.ECONNRESET, errno.ENOTCONN, errno.ETIMEDOUT ]:
                    msg._tell_dev(msg.M815_oserr_connection_error__errno_url, {"errno": str(myerrno)+":"+os.strerror(myerrno), "url": "tcp://"+_noapi_instance.tcp_host+":"+str(_noapi_instance.tcp_port)})
            except Exception as e:
                msg._tell_dev(msg.M711_unexpected_exception__exception, {"exception": e})

            _noapi_instance.websocket = TcpSocketAsWebSocket(tcpsocket)

        if 1:
            if not (datastore_url.startswith("datanet://")):
                datastore_url = "datanet://" + datastore_url

            datastore_url = "client="+self.client_version()+"/" + datastore_url
            localdbroot = "00000000"
            get_instance = _datanet_encode(
                _datanet_args(
                    {
                        "operation": "H",
                        "datatype": "str",
                        "oid": localdbroot,
                        "propid": "00000000",
                        "offset": "0000",
                        "text": datastore_url,
                    }
                )
            )
            console.debug(get_instance)
            _noapi_instance.first_response = self.__get_a_future()

            _noapi_instance.__receive_loop = asyncio.ensure_future(
                _noapi_instance.__the_receive_loop(_noapi_instance.websocket)
            )
            _noapi_instance.__register_resolve("00000000","00000000", _noapi_instance.first_response)
            await _noapi_instance.websocket.send(get_instance)

            # receive_loop alrady listening, so no need for next line
            # j = await websocket.recv()
            # print("first response was:")
            # print(j)

            tor = await Item._await_future(_noapi_instance.first_response)

            return tor

    async def __the_receive_loop(self, websocket: WebSocketAsWebSocket) -> None:
        while True:
            str_from_socket : Optional[str] = None
            try:
                str_from_socket = await websocket.recv()
            except(ConnectionClosedOK, ConnectionClosedError) as e: # FIXME: see what exception happens when connection is closed or on error
                pass
            except asyncio.CancelledError as e:
                pass
            except BaseException as e:
                raise

            try:
                if str_from_socket:
                    await self.__got_message(str_from_socket)
            except BaseException as e:
                print(e)
                # raise # DO NOT, since this will break the receive loop.
                # the developer will get the exception from resolve_data() instead
                # but we show it just in case s/he doesnt see it

    # FIXME: noapi appears not to be used!
    async def _destroy_on_server(
        self, myoid: str, mypropid: str, item: str
    ) -> Any:  # FIXME: be precise about return type
        cmd = _datanet_encode(
            _datanet_args(
                {
                    "operation": "X",
                    "datatype": "r-1",
                    "oid": myoid,
                    "propid": mypropid,
                    "target": item,
                }
            )
        )
        console.debug("cmd is:")
        console.debug(cmd)

        loop = asyncio.get_event_loop()
        resolve = self.__get_a_future()
        self.__register_resolve(myoid, mypropid + "D" + item, resolve)
        await self.websocket.send(cmd)
        destroyresult = await Item._await_future(resolve)
        return destroyresult

    # FIXME: noapi appears not to be used!
    async def _remove_on_server(
        self, myoid: str, mypropid: str, itemid: str,
    ) -> Any:  # FIXME: be precise about return type
        cmd = _datanet_encode(
            _datanet_args(
                {
                    "operation": "-",
                    "datatype": "r-1",
                    "oid": myoid,
                    "propid": mypropid,
                    "target": itemid
                }
            )
        )
        console.debug("cmd is:")
        console.debug(cmd)

        loop = asyncio.get_event_loop()
        resolve = self.__get_a_future()
        self.__register_resolve(myoid, mypropid + "R" + itemid, resolve)
        await self.websocket.send(cmd)
        removeresult = await Item._await_future(resolve)
        return removeresult

    # FIXME: noapi appears not to be used!
    async def _create_on_server(
        self,
        myoid: str,
        mypropid: str,
        set_value: Optional[str] = None,
        set_propname: Optional[str] = None,
    ) -> Any:  # FIXME: be precise about return type
        console.debug("create_on_server:")
        console.debug(mypropid)
        console.debug("of")
        console.debug(myoid)
        set_propid = (
            "00000000"  # FIXME: should this be related to set_propname, set_propvalue
        )
        if set_propname is not None:
            raise Exception("UNIMPLEMENTED setting property during create")
            # TODO: convert propname to id & set_value to objid for create

        cmd = _datanet_encode(
            _datanet_args(
                {
                    "operation": "$",
                    "datatype": "unk",
                    "oid": myoid,
                    "propid": mypropid,
                    "target": set_propid
                    # FIXME: need to also send set_value
                }
            )
        )
        console.debug("cmd is:")
        console.debug(cmd)

        loop = asyncio.get_event_loop()
        resolve = self.__get_a_future()
        # this future will be resolved, when
        # the data is received from server
        self.__register_resolve(myoid, mypropid + "N", resolve)  # + set_propid+val
        await self.websocket.send(cmd)
        createresult = await Item._await_future(resolve)
        return createresult

    async def _stop_server(self) -> None:
        cmd = _datanet_encode(
            _datanet_args(
                {
                    "operation": "Q",
                    "datatype": "unk",
                    "oid": "00000000",
                    "propid": "00000000",
                    "target": "00000000"
                    # FIXME: need to also send set_value
                }
            )
        )
        await self.websocket.send(cmd)

    async def _append_on_server(
        self, myoid: str, mypropid: str, item: str, before: bool = False, relative_to_item: Optional[str] = None
    ) -> Any:  # FIXME: be more precise about return type
        if relative_to_item is None:
            relative_str = "00000000" # hardcoded.none_itemid
        else:
            relative_str = relative_to_item
        if before:
            before_str = "BEFORE  "
        else:
            before_str = "AFTER   "
        cmd = _datanet_encode(
            _datanet_args(
                {
                    "operation": "I",
                    "datatype": "r-1",
                    "oid": myoid,
                    "propid": mypropid,
                    "blob": item+before_str+relative_str
                }
            )
        )
        console.debug("cmd is:")
        console.debug(cmd)

        loop = asyncio.get_event_loop()
        resolve = self.__get_a_future()
        # this future will be resolved, when
        # the data is received from server
        # FIXME: what if list is not appended to
        self.__register_resolve(myoid, mypropid, resolve)
        await self.websocket.send(cmd)
        appendresult = await Item._await_future(resolve)
        return appendresult

    async def __got_message(self, data: str) -> None:
        #x print("GOT MESSAGE, processing", data)
        try:
            response = _datanet_args(_datanet_decode(data))
            dataop = response.operation
            if dataop == "K":
                await self.__connected(response)
            elif dataop == "E":
                await self.__error_from_server(data)
            elif dataop == "=":
                await self.__got_assign(response)
            elif dataop == "N":
                await self.__got_new_item(response)
            # elif dataop == "W":
            #    await self.got_method_result(response)
            # elif dataop == "P":
            #    await self.got_prop_detail(response)
            elif dataop == "F":
                await self.__got_find_result(response)
            elif dataop == "D":
                await self.__got_destroy_result(response)
            elif dataop == "T":
                await self.__got_method_result(response)
            elif dataop == "R":
                await self.__got_remove_result(response)
            elif dataop == "0":
                pass
                # print("Got a no-op message from server")
            else:
                raise BaseException(
                    "Unknown operation >" + str(dataop) + "< from server"
                )
        except BaseException as e:
            # print("EXCEPTION in got_message")
            #print(e)
            #import traceback

            #traceback.print_exception(*sys.exc_info())
            #print("traceback stack:")
            #traceback.print_stack()
            raise
        #x print("DONE MESSAGE, processing", data)

    async def __connected(self, response: _datanet_args) -> None:
        appinstanceoid = response.oid
        typepropid = response.propid
        fieldspropid = "ERR-flds"
        if response.blob is not None:
            fieldspropid = response.blob[0:8]
            namepropid = response.blob[8:16]
            self._server_version_string = response.blob[16:]

        if appinstanceoid in self._localdb:
            console.debug("RECONNECT appo")
            appo = self._localdb[appinstanceoid]
            console.debug(appo)
            dso = appo
        else:
            console.debug("FIRSTCONNECT appo")
            try:
                dso = Item(self._localdb, appinstanceoid, self, True)
                ldb = self._localdb
                self.well_known_propids["type"] = typepropid
                self.well_known_propids["fields"] = fieldspropid
                self.well_known_propids["name"] = namepropid
            except:
                console.debug("CATCH")
                raise

            appo = dso  # was Proxy(dso,dso.proxyhander())
            console.debug("GOT APPO proxy")
            console.debug(appo)
            console.debug("SHOWED APPO")

        appinstance = self._localdb[appinstanceoid]
        datatype = response.datatype
        datavalue = response.target
        datapropid = response.propid

        console.debug("setup first appinstance")
        console.debug(appinstance)

        # return appInstace to getInstance(...)
        self._resolve_a_future(self.first_response, appinstance)

    async def _request_fieldvalue_from_server(
        self, myoid: str, mypropid: str, prevent_request: bool = False
    ) -> Any:  # FIXME: return should be something like a future?
        console.debug("getpfs:")
        console.debug(mypropid)
        console.debug("of")
        console.debug(myoid)
        console.debug(":getpfs")
        cmd = _datanet_encode(
            _datanet_args(
                {
                    "operation": "<",
                    "datatype": "unk",
                    "oid": myoid,
                    "propid": mypropid,
                    "target": "00000000",
                }
            )
        )

        console.debug(cmd)
        resolve = self.__get_a_future()

        # this future will be resolved, when
        # the oid:propid data is received from server
        requested = self.__check_resolve(myoid, mypropid)  # not already requested
        self.__register_resolve(myoid, mypropid, resolve)
        if not requested:
            await self.websocket.send(cmd)
            console.debug("sent")

        console.debug("made request to server")
        return resolve

    def __check_resolve(self, oid: str, propid: str) -> bool:
        if (
            (oid + ":" + propid in self.__data_resolver)
            and (self.__data_resolver[oid + ":" + propid] is not None)
            and len(self.__data_resolver[oid + ":" + propid])
        ) > 0:
            console.debug("resolve request already in place for " + oid + ":" + propid)
            return True

        console.debug("no request yet for " + oid + ":" + propid)
        return False

    def __register_resolve(
        self, oid: str, propid: str, func: Any
    ) -> None:  # FIXME: func is callable/awaitable?
        if not (oid + ":" + propid in self.__data_resolver):
            self.__data_resolver[oid + ":" + propid] = []

        self.__data_resolver[oid + ":" + propid].append(func)

    async def __data_resolve(
        self, oid: str, propid: str, data: Any
    ) -> bool:  # FIXME: can we be more precise about data Union[Exception,str] ?
        resolved=False
        if oid + ":" + propid in self.__data_resolver:
            console.debug("resolver exists")
            for f in self.__data_resolver[oid + ":" + propid]:
                console.debug(data)
                if isinstance(data, Exception):
                    f.set_exception(data)
                    resolved=True
                else:
                    console.debug("Resolved normally")
                    self._resolve_a_future(f, data)
                    resolved=True
                self.__data_resolver[oid + ":" + propid] = []

        # Also raise for exception if its not resolved
        if not resolved and isinstance(data, Exception):
            print("RAISING")
            print("resolver key not found: "+oid+":"+propid)
            print(data)
            raise data
        return resolved

    async def __error_from_server(self, response_str: str) -> None:
        response = _datanet_decode(response_str)
        # print("ERROR FROM SERVER IS:"+str(response["text"]))
        level = response["text"][0]
        error_code = response["text"][1:4]
        error_message = response["text"][4:]
        python_class: 'int|type' = Exception
        if level == 'W':
            python_class = Warning
        if level == 'D':
            python_class = DEBUG
        if level == 'I':
            python_class = INFO
        if level == 'T':
            python_class = DEBUG
        if level == 'N':
            python_class = NOTICE
        # other leves are Exception

        try:
            msg._tell_dev_detail(level,error_code,python_class, error_message, error_message)

        except Exception as the_exception:
            resolved = await self.__data_resolve(response["oid"], response["propid"], the_exception)
            if not resolved:
                if self.first_response is not None and not self.first_response.done():
                    self.first_response.set_exception(the_exception)
                    resolved = True
                else:
                    resolved = await self.__data_resolve(response["oid"], response["propid"], the_exception)
                if not resolved:
                    raise the_exception

    async def __got_assign(self, response: _datanet_args) -> None:
        datatype = response.datatype
        datablob = response.blob
        datatarget = response.target
        dataoid = response.oid
        datapropid = response.propid
        # dataoid may not exist in the database...
        if dataoid in self._localdb:
            Itemp = self._localdb[dataoid]
        else:
            Itemp = Item(self._localdb, dataoid, self, True)
            # i guess we trust the oid from the server

        if (
            datatype == "str"
            or datatype == "num"
            or datatype == "bol"
            or datatype == "nos"
            or datatype == "non"
            or datatype == "nob"
            or datatype == "nod"
        ):
            binitfunction = Itemp._setProperty
            initfunction = binitfunction  # partial(binitfunction,Itemp)
            newval: PropertyValue = None
            if response.text is not None:
                newval = response.text
            # fix newval into the right datatype
            if datatype == "bol":
                if newval == "true":
                    newval = True
                elif newval == "false":
                    newval = False
                else:
                    # FIXME: should this be a  throw
                    raise Exception(
                        "Server error: could not determin boolean value (true or false) from :"
                        + str(response.text)
                    )

            elif (
                datatype == "nob"
                or datatype == "nos"
                or datatype == "non"
                or datatype == "nod"
            ):
                newval = None

            elif datatype == "num":
                # try:
                #    setval=float(newval)
                #    if (int(setval)==int)newval)):
                #        setval=int(newval)
                # except:
                #    console.warn("Failed number conversion from:"+newval)
                #    newval=None
                try:
                    newval = float(newval)  # type: ignore # FIXME: how to do this to pass type checker correctly?
                except:
                    newval = None
            elif datatype == "str":
                # do nothing
                pass
            # no? means not a value
            elif datatype == "nos" or datatype == "nob" or datatype == "non":
                newval = None
            else:
                raise Exception(
                    "Server error: what kind of primitive is this:" + str(newval)
                )

            console.debug("newval")
            console.debug(newval)
            # this would set it on the server: Item[datapropid]=newval
            # we could do this quietly...
            await initfunction(datapropid, datatype, newval)
            await self.__data_resolve(dataoid, datapropid, newval)

        elif (datatype == "r-1") or (datatype == "noi"):
            # FIXME:  confusion between which response field, the received r-1 should be taken from. in target, or in blob? It is currently in the field called target, but comm protocol says otherwise
            #  target may does not needexist in the database.
            # it can be created when accessed?
            console.debug(response)

            # FIXME: strange case: box exists but is not created yet.
            if datatarget == "00000000":
                # FIXME: python: distinguish between UNKONWN and NOT SET
                newval = None
                datatype = "noi"
            else:
                newval = response.target

            if datatype == "noi":
                newval = None

            targetobj = newval
            setfunca = Itemp._setProperty
            setfuncb = setfunca  # partial(setfunca,Itemp)
            await setfuncb(datapropid, datatype, newval)
            # noapi[Itempt] = new Item(targetobj,objhandler)

            console.debug("RESPONSE TO R-1")
            console.debug({"r-1": targetobj})
            await self.__data_resolve(dataoid, datapropid, targetobj)

        elif (datatype == "r-n") or (datatype == "nol"):
            newval = response.blob
            if datatype == "nol":
                newval = None

            setfunca = Itemp._setProperty
            setfuncb = setfunca  # partial(setfunca,Itemp)
            targetobj = newval
            await setfuncb(datapropid, datatype, newval)
            # noapi[Itempt] = new Item(targetobj,objhandler)

            await self.__data_resolve(dataoid, datapropid, targetobj)  # ??
        elif datatype == "unk":
            await self.__data_resolve(
                dataoid, datapropid, msg.TellDevException(msg.M527_unknown_datatype_from_server,{})
            )
            msg._tell_dev(msg.M527_unknown_datatype_from_server,{})

        else:
            # throw "did not understand datatype:"+datatype
            console.error("did not understand datatype:" + datatype)


    async def _request_find_from_server(
        self, myoid: str, listpropid: str, search_for: str, in_field: str
    ) -> Optional[str]:
        console.debug("findpfs:")
        console.debug(listpropid)
        # console.trace()
        console.debug("of")
        console.debug(myoid)
        console.debug(":findpfs")
        cmd = _datanet_encode(
            _datanet_args(
                {
                    "operation": "S",
                    "datatype": "r-1",
                    "oid": myoid,
                    "propid": listpropid,
                    "text": in_field + search_for,
                }
            )
        )

        console.debug(cmd)
        # console.debug(noapi);

        resolve = self.__get_a_future()

        # this future will be resolved, when
        # the data is received from server
        requested = self.__check_resolve(
            myoid, listpropid + "_" + search_for
        )  # not already requested
        self.__register_resolve(myoid, listpropid + "_" + in_field + search_for, resolve)
        if not requested:
            await self.websocket.send(cmd)
            console.debug("made fps request to server")

        tor = await Item._await_future(resolve)
        console.debug("received fps reply from server")
        console.debug(repr(tor))
        return tor

    async def __got_find_result(self, response: _datanet_args) -> None:
        console.debug("GOT FIND RESULT MESSAGE")
        console.debug(response)
        datatype = response.datatype
        datablob = response.blob
        datatext = response.text
        datatarget = response.target
        dataoid = response.oid
        datapropid = response.propid
        if response.text is not None:
            search_str = response.text[8:]

        # dataoid may not exist in the database...
        # FIXME: Consider when return is not str!!
        if dataoid in self._localdb:
            Itemp = self._localdb[dataoid]
        else:
            Itemp = Item(self._localdb, dataoid, self, True)
            # i guess we trust the oid from the server

        console.debug("datatype")
        console.debug(datatype)
        if datatype == "r-1":
            # TODO: deviates from comm_spec: r_1 should be in target, not blob
            # easier for now, and matches the current server ipemenataion
            foundblob = response.blob
            if foundblob is not None:
                found_item_id = foundblob[:8]
            else:
                raise Exception("no blob when doing a find")
            target_item_id = found_item_id
            # TODO: the following will be  needed to cache search result
            console.debug("RESPONSE TO FIND got R-1")
            console.debug(
                {"r-1": target_item_id}
            )  # how could it work, targetobj not defined.
            await self.__data_resolve(dataoid, datapropid + "_" + search_str, target_item_id)
        elif datatype == "noi":
            console.debug("noi resolving")
            if response is not None and response.text is not None:
                search_str = response.text
            await self.__data_resolve(dataoid, datapropid + "_" + str(search_str), None)
        else:
            console.error("did not understand datatype:" + datatype)
            raise Exception("did not understand datatype:" + datatype)

    async def _call_method_on_server(
        self, myoid: str, method_name: str, args: Dict[str,Optional[str]]) -> Dict[str,Optional[str]]:
        console.debug("call_method_on_server:")
        console.debug(args)
        # console.trace()
        console.debug("of")
        console.debug(myoid)
        # transaction_id = "T"+''.join(random.choices(string.ascii_uppercase + string.digits, k=7))
        # adapted for micropython as:
        transaction_id = "T"+str('%07x' % random.getrandbits(32)).upper()[0:7]

        # method_len = "{:08}".format(len(method_name))
        # strargs = method_len + method_name + chr(0)
        # for (arg_name, arg_val) in args.items():
        #     strargs += arg_name + chr(0) + arg_val + chr(0)
        # offset = 8+8+len(args)*16 # argcount + length of method_name + (8 start+8len)=16 char each arg
        # method_offset_str =  "{:08}".format(offset)
        # countargs = "{:08}".format(1+len(args))
        # countargs += method_offset_str
        # offset += len(method_name) + 1
        # for (arg_name, arg_val) in args.items():
        #     countargs += "{:08d}".format(len(arg_name))
        #     countargs += "{:08d}".format(len(arg_val))
        # text = countargs +  strargs
        text = _datanet_args_encode(method_name, args)
        cmd = _datanet_encode(
            _datanet_args(
                {
                    "operation": "M",
                    "datatype": "str",
                    "oid": myoid,
                    "propid": transaction_id,
                    "text": text
                }
            )
        )

        resolve = self.__get_a_future()

        # this future will be resolved, when
        # the data is received from server
        key = transaction_id  # FIXME: trabscation_id and propid use the same space. txid might ve the same as a propid.
        requested = self.__check_resolve(
            myoid, key
        )  # not already requested
        self.__register_resolve(myoid, key, resolve)
        if not requested:
            await self.websocket.send(cmd)
            console.debug("made method request to server")

        tor = await Item._await_future(resolve)
        console.debug("received method reply from server")
        console.debug(repr(tor))
        return tor

    async def __got_method_result(self, response: _datanet_args) -> None:
        console.debug("GOT FIND RESULT MESSAGE")
        console.debug(response)
        datatype = response.datatype
        datablob = response.blob
        datatext = response.text
        datatarget = response.target
        dataoid = response.oid
        datapropid = response.propid
        if response.text is not None:
            method_result_str = response.text

        # dataoid may not exist in the database...
        # FIXME: Consider when return is not str!!
        if dataoid in self._localdb:
            Itemp = self._localdb[dataoid]
        else:
            Itemp = Item(self._localdb, dataoid, self, True)
            # i guess we trust the oid from the server

        console.debug("datatype")
        console.debug(datatype)
        if datatype == "arg":
            # TODO: arg deviates from spec. arg should be standardized
            args = _datanet_args_decode(method_result_str)

            await self.__data_resolve(dataoid, datapropid, args) # FIXME: datapropid might be a real propid instead of transcation id
        elif datatype == "noi":
            console.debug("noi resolving")
            if response is not None and response.text is not None:
                search_str = response.text
            await self.__data_resolve(dataoid, "method_"+ datapropid, None)
        else:
            console.error("did not understand datatype:" + datatype)
            raise Exception("did not understand datatype:" + datatype)

    async def __got_new_item(self, response: _datanet_args) -> None:
        console.debug("GOT NEW ITEM")
        console.debug(response)
        datatype = response.datatype
        datablob = response.blob
        datatext = response.text
        datatarget = response.target
        dataoid = response.oid
        datapropid = response.propid
        if datatype == "r-1":
            # FIXME: check length of blob.
            if datablob is not None and (response.length == 9):
                datablob8 = datablob[0:8]
            else:
                raise Exception(
                    f"received no blob when creating item of length {response.length}"
                )
            newobj = datablob8
            await self.__data_resolve(dataoid, datapropid + "N", datablob8)
            # FIXME: case when prop is set
            # /* + datablob.substr(8, 8) */,
        elif datatype == "noi":
            console.debug("noi resolving")
            print("FAILED new item")
            await self.__data_resolve(
                dataoid,
                datapropid + "N",
                Exception("could not create item:" + str(datatext)),
            )
        else:
            console.error("did not understand datatype:" + datatype)
            raise Exception("did not understand datatype:" + datatype)

    async def __got_destroy_result(self, response: _datanet_args) -> None:
        datatype = response.datatype
        datablob = response.blob
        datatext = response.text
        datatarget = response.target
        dataoid = response.oid
        datapropid = response.propid
        datablob8 = ""
        if datatype == "noi":
            await self._localdb[datatarget]._destroy_locally()
            await self.__data_resolve(dataoid, datapropid + "D" + datatarget, True)
        elif datatype == "r-1":
            if datablob is not None:
                datablob8 = datablob[0:8]
            else:
                raise Exception("got no blob when destroying an item")
            console.debug("FAILED destroy")
            if datatext is None:
                datatext = "ERR-Info"
            await self.__data_resolve(
                dataoid, datapropid + "D" + datablob8, Exception(datatext[8:])
            )
        else:
            console.error("did not understand datatype:" + datatype)
            raise Exception("did not understand datatype:" + datatype)

    async def __got_remove_result(self, response: _datanet_args) -> None:
        datatype = response.datatype
        datablob = response.blob
        datatext = response.text
        datatarget = response.target
        dataoid = response.oid
        datapropid = response.propid
        datablob8 = ""
        if datatype == "noi":
            await self.__data_resolve(dataoid, datapropid + "R" + datatarget, True)
        elif datatype == "r-1":
            if datablob is not None:
                datablob8 = datablob[0:8]
            else:
                raise Exception("got no blob when removing an item")
            console.debug("FAILED remove")
            if datatext is None:
                datatext = "ERR-Info"
            await self.__data_resolve(
                dataoid, datapropid + "R" + datablob8, Exception(datatext[8:])
            )
        else:
            console.error("did not understand datatype:" + datatype)
            raise Exception("did not understand datatype:" + datatype)

    async def _set_field_on_server(
        self,
        myoid: str,
        mypropid: str,
        new_value: Union[Item, PropertyValue],
        datatype: str,
    ) -> Item:
        console.debug("setpfs:")
        console.debug(mypropid)
        console.debug("of")
        console.debug(myoid)
        console.debug("to:")
        console.debug(new_value)
        console.debug(":setpfs")

        text = str(new_value)
        console.debug("text")
        console.debug(text)

        cmd = _datanet_encode(
            _datanet_args(
                {
                    "operation": ">",
                    "datatype": datatype,
                    "oid": myoid,
                    "propid": mypropid,
                    "text": text,
                }
            )
        )

        console.debug("cmd is:")
        console.debug(cmd)

        # this future will be resolved, when
        # the data is received from server
        resolve = self.__get_a_future()
        # FIXME: the update message should contain some unique id. The server should respond that it processed this update request with this nique id.
        self.__register_resolve(myoid, mypropid, resolve)
        await self.websocket.send(cmd)
        console.debug("made set request to server")
        setresult = await Item._await_future(resolve)
        console.debug("got set result:" + str(setresult))
        return setresult

    @staticmethod
    async def __noapimain(f: Any) -> Any:  # FIXME: f should be something like a coroutine?
        no_inspect = True
        try:
            import inspect
            no_inspect = False
        except:
            pass

        if not no_inspect:
            if inspect.isawaitable(f):
                tor = await asyncio.gather(f)
            else:
                tor = f()
                if inspect.isawaitable(tor):
                    tor = await tor
            disconnect()
        else:
            tor = await tor
            disconnect()

        return tor

    @staticmethod
    def run(cls: "noapi",mainf: Any= None) -> Any:  # FIXME: mainf should be someting like callable/coroutine?
        if type(cls) is not noapi:
            mainf = cls
        # asyncio.get_event_loop().run(noapimain(f))
        keyboard_interruptexception = None
        try:
            return asyncio.run(noapi.__noapimain(mainf))  # type: ignore # FIXME: figure out typing parameters
            # pasyncio.get_event_loop().run_until_complete(mainf())
            # asyncio.run(noapimain(mainf))
            # noapimain(mainf())
        except KeyboardInterrupt as e:
            keyboard_interruptexception = e
        except TypeError as e:
            msg._handle_native_exception(e)
            sys.exit(1)
        except AttributeError as e:
            msg._handle_native_exception(e)
            sys.exit(1)
        except Exception as e:
            msg._handle_native_exception(e)
            sys.exit(1)
        if keyboard_interruptexception:
            raise KeyboardInterrupt

def run(mainf: Any) -> Any: # FIXME: mainf should be someting like callable/coroutine?
    return noapi.run(mainf)

def datastore(datastore_url: str) -> Item:   # when used as noapi.datastore(xx)
    _noapi_instance = noapi._noapi_instance
    if _noapi_instance is None:
        _noapi_instance = noapi()
    return _noapi_instance.datastore(datastore_url)

def client_version() -> str:
    return noapi.client_version()
def server_version() -> Optional[str]:
    """implements :py:meth:`noapi_ref.Noapi.server_version`"""
    if noapi._noapi_instance is None:
        return None
    return noapi._noapi_instance.server_version()
def set_websocket(ws_url: str) -> None:
    """implements :py:meth:`noapi_ref.Noapi.set_websocket`"""
    if noapi._noapi_instance is None:
        noapi._noapi_instance = noapi(ws_url)
    else:
        raise Exception("noapi was already constructed with another websocket url")

def disconnect() -> None:
    if noapi._noapi_instance is None:
        return None
    _await_async(noapi._noapi_instance._async_disconnect())

def _stop_server() -> None:
    if noapi._noapi_instance is None:
        return None
    _await_async(noapi._noapi_instance._stop_server())
