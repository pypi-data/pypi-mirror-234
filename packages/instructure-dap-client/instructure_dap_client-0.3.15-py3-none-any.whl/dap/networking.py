import socket
import sys
from dataclasses import dataclass
from email.message import Message
from typing import Dict, List, Tuple, Optional

from aiohttp import ClientRequest, ClientResponse, ClientError
from aiohttp.connector import Connection


@dataclass
class ParseContentResult:
    """
    Results of parsing an HTTP `Content-Type` header.

    :param content_type: The extracted content type such as "application/json".
    :param attributes: Other key=value attribute pairs such as "charset=UTF-8".
    """

    content_type: str
    attributes: Dict[str, str]


def parse_content_type(content_type_header: str) -> ParseContentResult:
    "Parses an HTTP `Content-Type` header."

    email = Message()
    email["Content-Type"] = content_type_header
    params: List[Tuple[str, str]] = email.get_params(
        failobj=[("application/octet-stream", "")]
    )
    return ParseContentResult(params[0][0], dict(params[1:]))


def get_content_type(content_type_header: str) -> str:
    result = parse_content_type(content_type_header)
    return result.content_type


class KeepAliveClientRequest(ClientRequest):
    async def send(self, conn: Connection) -> ClientResponse:
        from aiohttp.client_proto import ResponseHandler
        protocol: Optional[ResponseHandler] = conn.protocol
        if protocol is None:
            raise KeepAliveClientRequestError("Connection has no protocol.")
        transport = protocol.transport
        if transport is None:
            raise KeepAliveClientRequestError("Protocol has no transport.")
        sock = transport.get_extra_info("socket")
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_KEEPALIVE, 1)
        if sys.platform != "darwin":
            sock.setsockopt(socket.IPPROTO_TCP, socket.TCP_KEEPIDLE, 60)
        sock.setsockopt(socket.IPPROTO_TCP, socket.TCP_KEEPINTVL, 2)
        sock.setsockopt(socket.IPPROTO_TCP, socket.TCP_KEEPCNT, 5)

        return await super().send(conn)


class KeepAliveClientRequestError(ClientError):
    """
    Raised when a keep-alive request is attempted on a connection that has no protocol or transport.
    """
