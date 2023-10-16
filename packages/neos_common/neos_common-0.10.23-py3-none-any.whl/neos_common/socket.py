import asyncio
import json
import logging
import socket
import socketserver
import time
import typing

import pydantic
import pydantic.error_wrappers

from neos_common import error, schema

if typing.TYPE_CHECKING:
    Loc = typing.Tuple[typing.Union[int, str], ...]

    class _ErrorDictRequired(typing.TypedDict):
        loc: Loc
        msg: str
        type: str

    class ErrorDict(_ErrorDictRequired, total=False):
        """Type hint for pydantic.error_wrappers.ErrorDict.

        Stolen from type hints in pydantic.error_wrappers
        """

        ctx: typing.Dict[str, typing.Any]


logger = logging.getLogger(__name__)


Socket = socket.socket


class SocketException(Exception):  # noqa: N818
    """Base class for all socket exceptions."""

    status = "unhandled"

    def __init__(self, reason: str, message: str, details: typing.Union[typing.List["ErrorDict"], None]) -> None:
        """Socket exception initiator.

        Args:
        ----
        reason: error reason i.e. "NOT_FOUND"
        message: error message
        details: optional list of pydantic validation errors
        """
        self.reason = reason
        self.message = message
        self.details = details

    def __iter__(self) -> typing.Iterator[typing.Tuple[str, typing.Union[bool, str, typing.List["ErrorDict"], None]]]:
        """Return an iterator to support `dict(self)`."""
        return iter(
            [
                ("ok", False),
                ("status", self.status),
                ("reason", self.reason),
                ("message", self.message),
                ("details", self.details),
            ],
        )


class ValidationError(SocketException):
    status = "validation_error"


def encode(obj: dict, encoder: typing.Union[typing.Type[json.JSONEncoder], None] = None) -> bytes:
    """JSON encode message object for sending via socket."""
    new = json.dumps(obj, cls=encoder)
    return new.encode()


def decode(obj: typing.Union[bytes, None]) -> typing.Union[typing.Dict[str, typing.Any], None]:
    """Decode message received via socket."""
    if obj is None:
        return obj

    data: typing.Dict[str, typing.Any] = json.loads(obj.decode())
    return data


class AsyncSocket:
    def __init__(self, reader: asyncio.streams.StreamReader, writer: asyncio.streams.StreamWriter) -> None:
        self.reader = reader
        self.writer = writer

    def write(self, msg: bytes) -> None:
        """Send a message via the socket."""
        msg = add_msg_header(msg)
        self.writer.write(msg)

    async def read(self) -> typing.Union[typing.Dict, None]:
        """Receive a message via the socket."""
        # start by getting the header
        # (which is an int of length `BYTE_COUNT`).
        # The header tells the message size in bytes.
        raw_msglen = await self.reader.read(BYTE_COUNT)
        # Then retrieve a message of length `raw_msglen`
        # this will be the actual message
        msglen = len_frombytes(raw_msglen)

        data = bytearray()
        while len(data) < msglen:
            packet = await self.reader.read(msglen - len(data))
            if not packet:
                return None
            data.extend(packet)

        return decode(data)

    def close(self) -> None:
        self.writer.close()


BYTE_COUNT = 4


def send_msg(sock: Socket, msg: bytes) -> None:
    """Send a message via the socket."""
    msg = add_msg_header(msg)
    sock.sendall(msg)


def recv_msg(sock: Socket) -> typing.Union[bytearray, None]:
    """Receive a message via the socket."""
    # start by getting the header
    # (which is an int of length `BYTE_COUNT`).
    # The header tells the message size in bytes.
    raw_msglen = recvall(sock, BYTE_COUNT)
    if not raw_msglen:
        return None
    # Then retrieve a message of length `raw_msglen`
    # this will be the actual message
    msglen = len_frombytes(raw_msglen)
    return recvall(sock, msglen)


def recvall(sock: Socket, length: int) -> typing.Union[bytearray, None]:
    """Get a message of a certain length from the socket stream."""
    data = bytearray()
    while len(data) < length:
        packet = sock.recv(length - len(data))
        if not packet:
            return None
        data.extend(packet)
    return data


def add_msg_header(msg: bytes) -> bytes:
    """Prepend message length header onto message.

    Args:
    ----
    msg: message bytestring

    Returns:
    -------
    new bytestring with original message length prepended.
    """
    return len_inbytes(msg) + msg


def len_inbytes(msg: bytes) -> bytes:
    """Retrieve length of message as a bytestring."""
    return len(msg).to_bytes(BYTE_COUNT, byteorder="big")


def len_frombytes(bmsg: bytes) -> int:
    """Extract length of message from a bytestring header."""
    return int.from_bytes(bmsg, byteorder="big")


class AsyncTCPHandler:
    Request = schema.SocketRequest

    async def setup(self) -> None:
        ...

    async def teardown(self) -> None:
        ...

    async def __call__(self, reader: asyncio.streams.StreamReader, writer: asyncio.streams.StreamWriter) -> None:
        async_socket = AsyncSocket(reader, writer)
        await self.setup()
        try:
            data = await async_socket.read()
        except json.decoder.JSONDecodeError as e:
            logger.exception("Decode error processing request.")
            exc = ValidationError(
                reason="DecodeError",
                message=str(e),
                details=None,
            )
            async_socket.write(encode(dict(exc)))
        except Exception as e:
            logger.exception("Exception processing request.")
            exc = SocketException(
                reason="Unhandled",
                message=str(e),
                details=None,
            )
            async_socket.write(encode(dict(exc)))
        else:
            if data is None:
                await self.teardown()
                async_socket.close()
                return

            try:
                request = self.Request(**data)
                request_type = request.request_type

                RequestDataCls = self.request_mapping.get(request_type, dict)  # noqa: N806
                request_data = RequestDataCls(**request.data)
            except pydantic.ValidationError as e:
                logger.exception("Validation error processing request data.")
                exc = ValidationError(
                    reason="ValidationError",
                    message="Unable to parse message.",
                    details=e.errors(),
                )
                async_socket.write(encode(dict(exc)))
            except Exception as e:
                logger.exception("Exception processing request data.")
                exc = SocketException(
                    reason="Unhandled",
                    message=str(e),
                    details=None,
                )
                async_socket.write(encode(dict(exc)))
            else:
                await self._handle(async_socket, request_type, request_data)

        await self.teardown()
        async_socket.close()

    async def _handle(
        self,
        sock: AsyncSocket,
        request_type: str,
        request_data: typing.Union[pydantic.BaseModel, dict],
    ) -> None:
        ...


class TCPHandler(socketserver.BaseRequestHandler):
    """Base handler for TCP socket server.

    When a message is received:
        * decode it
        * format it into an instance of `cls.Request`
        * pass it to the handler defined for `request.request_type` in `cls.request_mapping`

    Define the mapping between Request.request_typpe and handlers in `cls.request_mapping`.
    Override the default SocketRequest schema via `cls.Request`
    """

    request_mapping: typing.ClassVar[dict] = {}
    Request = schema.SocketRequest

    def handle(self) -> None:
        """Handle an incoming request.

        Handle issues decoding, processing and validating request messages, on
        error response to the client, with error details.

        On success pass the validated request message to the appropriate
        handler.
        """
        try:
            data = decode(recv_msg(self.request))
        except json.decoder.JSONDecodeError as e:
            logger.exception("Decode error processing request.")
            exc = ValidationError(
                reason="DecodeError",
                message=str(e),
                details=None,
            )
            send_msg(self.request, encode(dict(exc)))
        except Exception as e:
            logger.exception("Exception processing request.")
            exc = SocketException(
                reason="Unhandled",
                message=str(e),
                details=None,
            )
            send_msg(self.request, encode(dict(exc)))
        else:
            if data is None:
                return

            try:
                request = self.Request(**data)
                request_type = request.request_type

                RequestDataCls = self.request_mapping.get(request_type, dict)  # noqa: N806
                request_data = RequestDataCls(**request.data)
            except pydantic.ValidationError as e:
                logger.exception("Validation error processing request data.")
                exc = ValidationError(
                    reason="ValidationError",
                    message="Unable to parse message.",
                    details=e.errors(),
                )
                send_msg(self.request, encode(dict(exc)))
            except Exception as e:
                logger.exception("Exception processing request data.")
                exc = SocketException(
                    reason="Unhandled",
                    message=str(e),
                    details=None,
                )
                send_msg(self.request, encode(dict(exc)))
            else:
                self._handle(self.request, request_type, request_data)

    def _handle(self, sock: Socket, request_type: str, request_data: typing.Union[pydantic.BaseModel, dict]) -> None:
        ...


class AsyncTCPClient:
    """Base implementation for asyncio stream socket service client."""

    def __init__(
        self,
        host: str,
        port: int,
        encoder: typing.Union[typing.Type[json.JSONEncoder], None] = None,
    ) -> None:
        """TCPClient instantiator.

        Args:
        ----
        host: socket service host name
        port: socket service port
        encoder: json encoder for request messages
        """
        self.addr = (host, port)
        self.encoder = encoder

    async def send_request(self, request: dict) -> dict:
        """Send a request to socket service.

        Handle socket connection errors, and response timeouts.
        """
        try:
            reader, writer = await asyncio.open_connection(*self.addr)
            async_socket = AsyncSocket(reader, writer)
        except OSError as e:
            raise error.ServiceConnectionError(
                message="Unable to connect to service.",
                debug_message=f"{self.addr}: {e!s}",
            ) from e

        try:
            async_socket.write(encode(request, encoder=self.encoder))
            response = await async_socket.read()
        finally:
            async_socket.close()

        return response


class TCPClient:
    """Base implementation for socket service client."""

    def __init__(
        self,
        host: str,
        port: int,
        timeout: int = 10,
        wait: int = 10,
        encoder: typing.Union[typing.Type[json.JSONEncoder], None] = None,
    ) -> None:
        """TCPClient instantiator.

        Args:
        ----
        host: socket service host name
        port: socket service port
        timeout: number of seconds to wait for a connection
        wait: number of seconds to wait for a response from service
        encoder: json encoder for request messages
        """
        self.addr = (host, port)
        self.timeout = timeout
        self.wait = wait
        self.encoder = encoder

    def send_request(self, request: dict) -> dict:
        """Send a request to socket service.

        Handle socket connection errors, and response timeouts.
        """
        t0 = time.time()
        try:
            sock = socket.create_connection(
                self.addr,
                timeout=self.timeout,
            )
        except socket.gaierror as e:
            raise error.ServiceConnectionError(
                message="Unable to connect to service.",
                debug_message=f"{self.addr}: {e!s}",
            ) from e

        try:
            send_msg(sock, encode(request, encoder=self.encoder))
            t0 = time.time()
            response = None
            while not response:
                try:
                    response = decode(recv_msg(sock))
                except Exception as e:  # noqa: BLE001
                    raise error.ServiceConnectionError(
                        message="Unable to process request to service.",
                        debug_message=f"{self.addr}: {e.__class__.__name__}({e!s})",
                    ) from e
                if time.time() - t0 > self.wait:
                    msg = "Timed out waiting for resp."
                    raise TimeoutError(msg)
        finally:
            sock.close()
        return response
