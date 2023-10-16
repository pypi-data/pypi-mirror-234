import json
import logging
import typing
from datetime import datetime, timezone
from enum import Enum

import httpx
import requests

from neos_common import error
from neos_common.authorization import signer

RequestType = typing.TypeVar("RequestType", httpx.Request, requests.Request)

logger = logging.getLogger(__name__)


BAD_REQUEST_CODE = 400
REQUEST_VALIDATION_CODE = 422
RATE_LIMIT_CODE = 429


class Method(Enum):
    """HTTP request methods."""

    GET = "GET"
    POST = "POST"
    PUT = "PUT"
    DELETE = "DELETE"


async def log_request(request: httpx.Request) -> None:
    """Event hook for httpx events to log requests."""
    logger.info(
        f"[Request] {request.method.upper()} {request.url}",
    )


class NeosBearerClientAuth:
    def __init__(self, token: str) -> None:
        self.token = token

    def __call__(self, request: RequestType) -> RequestType:
        request.headers["Authorization"] = f"Bearer {self.token}"
        return request

    def __eq__(self, other: object) -> bool:  # noqa: D105
        return isinstance(other, NeosBearerClientAuth) and other.token == self.token


class NeosSignatureClientAuth:
    """HTTP client authentication class for NEOS rest services."""

    def __init__(self, key_pair: signer.KeyPair, service: str) -> None:
        self.key_pair = key_pair
        self.service = service

    def __call__(self, request: RequestType) -> RequestType:

        dt = datetime.now(tz=timezone.utc)
        request.headers["x-neos-date"] = signer.to_amz_date(dt)
        request.headers["host"] = request.url.netloc.decode("utf-8")

        body = request.content.decode("utf-8")
        if body:
            request.headers["Content-Length"] = str(len(body))

        s = signer.Signer("NEOS4-HMAC-SHA256")
        s.sign_v4(
            self.service,
            request.method,
            request.url,
            self.key_pair.partition,
            request.headers,
            self.key_pair,
            body,
            dt,
        )

        return request

    def __eq__(self, other: object) -> bool:  # noqa: D105
        return isinstance(other, NeosSignatureClientAuth) and other.key_pair == self.key_pair


class NeosClient(typing.Protocol):
    """Base class for HTTP client implementations for NEOS rest services."""

    unhandled_error_class = error.UnhandledServiceApiError
    handled_error_class = error.ServiceApiError

    @property
    def token(self) -> typing.Union[str, None]:
        ...

    @property
    def key_pair(self) -> typing.Union[signer.KeyPair, None]:
        ...

    @property
    def known_errors(self) -> typing.Set[str]:
        ...  # pragma: no cover

    @property
    def service_name(self) -> str:
        ...  # pragma: no cover

    async def _request(
        self,
        url: str,
        method: Method,
        params: typing.Union[dict, None] = None,
        headers: typing.Union[dict, None] = None,
        json: typing.Union[dict, None] = None,
        *,
        verify: bool = True,
        **kwargs,
    ) -> httpx.Response:
        if self.key_pair is not None:
            auth = NeosSignatureClientAuth(
                self.key_pair,
                self.service_name,
            )
        elif self.token:
            auth = NeosBearerClientAuth(self.token)
        else:
            auth = None

        async with httpx.AsyncClient(event_hooks={"request": [log_request]}, verify=verify) as client:
            try:
                r = await client.request(
                    url=url,
                    method=method.value,
                    params=params,
                    json=json,
                    headers=headers,
                    auth=auth,
                    **kwargs,
                )
            except httpx.ConnectError as e:
                raise error.ServiceConnectionError(
                    message=f"Error connecting to {self.service_name} service.",
                    debug_message=str(e),
                ) from e

        return r

    async def _get(
        self,
        url: str,
        params: typing.Union[dict, None] = None,
        headers: typing.Union[dict, None] = None,
    ) -> httpx.Response:
        return await self._request(
            url=url,
            method=Method.GET,
            params=params,
            headers=headers,
        )

    async def _post(
        self,
        url: str,
        json: typing.Union[dict, None] = None,
        headers: typing.Union[dict, None] = None,
    ) -> httpx.Response:
        return await self._request(
            url=url,
            method=Method.POST,
            json=json,
            headers=headers,
        )

    async def _put(
        self,
        url: str,
        json: typing.Union[dict, None] = None,
        headers: typing.Union[dict, None] = None,
    ) -> httpx.Response:
        return await self._request(
            url=url,
            method=Method.PUT,
            json=json,
            headers=headers,
        )

    async def _delete(
        self,
        url: str,
        json: typing.Union[dict, None] = None,
        headers: typing.Union[dict, None] = None,
    ) -> httpx.Response:
        return await self._request(
            url=url,
            method=Method.DELETE,
            json=json,
            headers=headers,
        )

    def process_response(self, response: httpx.Response) -> dict:
        try:
            data = response.json()
        except json.JSONDecodeError as exc:
            logger.error(response.content)  # noqa: TRY400
            raise self.unhandled_error_class(
                message=f"Invalid {self.service_name} api JSON format response.",
                status=response.status_code,
                code=None,
                debug_message=f"{exc.msg}: {exc.pos}",
            ) from exc
        if response.status_code >= BAD_REQUEST_CODE:
            logger.info(data)
            try:
                debug_message = None
                if data["code"] is not None:
                    debug_message = data.get("debug_message", data["message"])

                exc = self.unhandled_error_class(
                    message=f"Unhandled {self.service_name} api error response.",
                    status=response.status_code,
                    code=data["code"],
                    debug_message=debug_message,
                )
            except KeyError as e:
                exc = self.unhandled_error_class(
                    message=f"Unhandled {self.service_name} api response.",
                    status=response.status_code,
                    code=None,
                    debug_message=None,
                )
                if response.status_code == RATE_LIMIT_CODE:
                    exc = self.unhandled_error_class(
                        message=f"{self.service_name} api rate limit error.",
                        status=response.status_code,
                        code=None,
                        debug_message=None,
                    )

                raise exc from e

            if response.status_code == REQUEST_VALIDATION_CODE:
                exc = self.handled_error_class(
                    message=f"{self.service_name} request validation error.",
                    debug_message=data.get("debug_message"),
                    code=data["code"],
                    status=response.status_code,
                )
            elif data["code"] in self.known_errors:
                exc = self.handled_error_class(
                    message=data["message"],
                    debug_message=data.get("debug_message"),
                    code=data["code"],
                    status=response.status_code,
                )

            raise exc

        return data
