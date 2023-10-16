import hashlib
import hmac
import logging
import re
import typing
import urllib.parse
from collections import OrderedDict
from datetime import datetime, timezone

import httpx
import multidict

from neos_common import error

logger = logging.getLogger(__name__)


class KeyPair(typing.NamedTuple):
    access_key_id: "str"
    secret_access_key: "str"
    partition: "str"


_MULTI_SPACE_REGEX = re.compile(r"( +)")


def _quote(
    resource: str,
    safe: str = "/",
    encoding: typing.Union[str, None] = None,
    errors: typing.Union[str, None] = None,
) -> str:
    return urllib.parse.quote(
        resource,
        safe=safe,
        encoding=encoding,
        errors=errors,
    ).replace("%7E", "~")


def _to_utc(value: datetime) -> datetime:
    """Convert to UTC time if value is not naive."""
    return value.astimezone(timezone.utc).replace(tzinfo=None) if value.tzinfo else value


def to_amz_date(value: datetime) -> str:
    """Format datetime into AMZ date formatted string."""
    return _to_utc(value).strftime("%Y%m%dT%H%M%SZ")


def to_signer_date(value: datetime) -> str:
    """Format datetime into SignatureV4 date formatted string."""
    return _to_utc(value).strftime("%Y%m%d")


def sha256_hash(data: typing.Union[bytes, str, None]) -> str:
    """Compute SHA-256 of data and return hash as hex encoded value."""
    data = data or b""
    data_ = data.encode() if isinstance(data, str) else data
    hasher = hashlib.sha256()
    hasher.update(data_)
    sha256sum = hasher.hexdigest()
    return sha256sum.decode() if isinstance(sha256sum, bytes) else sha256sum


def _hmac_hash(
    key: typing.Union[bytes, bytearray],
    data: bytes,
    *,
    hexdigest: bool = False,
) -> typing.Union[str, bytes]:
    """Return HMacSHA256 digest of given key and data."""
    hasher = hmac.new(key, data, hashlib.sha256)
    return hasher.hexdigest() if hexdigest else hasher.digest()


def _generate_canonical_headers(headers: multidict.CIMultiDict) -> typing.Tuple[str, str]:
    """Get canonical headers."""
    canonical_headers = {}
    for key, values in headers.items():
        key_ = key.lower()
        if key_ not in ("authorization", "user-agent", "accept", "accept-encoding", "connection"):
            values_ = values if isinstance(values, (list, tuple)) else [values]
            canonical_headers[key_] = ",".join([_MULTI_SPACE_REGEX.sub(" ", value) for value in values_])

    canonical_headers = OrderedDict(sorted(canonical_headers.items()))
    signed_headers = ";".join(canonical_headers.keys())
    canonical_headers = "\n".join(
        [f"{key}:{value}" for key, value in canonical_headers.items()],
    )
    return canonical_headers, signed_headers


def _recreate_canonical_headers(headers: multidict.CIMultiDict, signed_headers: str) -> str:
    """Get canonical headers from SignedHeaders."""
    signed_headers_ = signed_headers.split(";")
    canonical_headers = {}
    for key, values in headers.items():
        key_ = key.lower()
        if key_ in signed_headers_:
            values_ = values if isinstance(values, (list, tuple)) else [values]
            canonical_headers[key_] = ",".join([_MULTI_SPACE_REGEX.sub(" ", value) for value in values_])

    canonical_headers = dict(sorted(canonical_headers.items()))
    return "\n".join(
        [f"{key}:{value}" for key, value in canonical_headers.items()],
    )


def _generate_canonical_query_string(query: typing.Union[bytes, str]) -> str:
    """Get canonical query string."""
    query = query or ""
    query_: str = query.decode() if isinstance(query, bytes) else query
    return "&".join(
        [
            "=".join(pair)
            for pair in sorted(
                [params.split("=") for params in query_.split("&")],
            )
        ],
    )


def _generate_signing_key(
    schema: str,
    secret_key: str,
    date: str,
    partition: str,
    service_name: str,
) -> typing.Union[str, bytes]:
    """Get signing key."""
    logger.debug(f"signing_key schema: {schema}")
    date_key = _hmac_hash(
        (schema + secret_key).encode(),
        date.encode(),
    )
    date_region_key = _hmac_hash(date_key, partition.encode())
    date_region_service_key = _hmac_hash(
        date_region_key,
        service_name.encode(),
    )
    return _hmac_hash(date_region_service_key, f"{schema.lower()}_request".encode())


def _generate_signature(signing_key: typing.Union[str, bytes], string_to_sign: str) -> typing.Union[str, bytes]:
    """Get signature."""
    return _hmac_hash(signing_key, string_to_sign.encode(), hexdigest=True)


class Signer:
    def __init__(self, auth_type: str) -> None:
        self.auth_type = auth_type
        self.auth_schema = auth_type.split("-")[0]
        self.header_prefix = "x-neos" if self.auth_schema == "NEOS4" else "x-amz"

    @staticmethod
    def _generate_scope(schema: str, date: datetime, partition: str, service_name: str) -> str:
        """Get scope string."""
        return f"{to_signer_date(date)}/{partition}/{service_name}/{schema.lower()}_request"

    @staticmethod
    def _generate_string_to_sign(auth_type: str, date: datetime, scope: str, canonical_request_hash: str) -> str:
        """Get string-to-sign."""
        return f"{auth_type}\n{to_amz_date(date)}\n{scope}\n{canonical_request_hash}"

    @staticmethod
    def _generate_canonical_request_hash(
        method: str,
        url: httpx.URL,
        headers: multidict.CIMultiDict,
        content_sha256: str,
    ) -> typing.Tuple[str, str]:
        """Get canonical request hash.

        https://docs.aws.amazon.com/IAM/latest/UserGuide/create-signed-request.html

        Create a canonical request by concatenating the following strings, separated by newline characters.
        This helps ensure that the signature that you calculate and the signature that the server calculates can match.

            HTTPMethod
            CanonicalUri
            CanonicalQueryString
            CanonicalHeaders
            SignedHeaders
            HashedPayload

        HTTPMethod -
            The HTTP method.

        CanonicalUri -
            The URI-encoded version of the absolute path component URL
            (everything between the host and the question mark character (?) that starts the query string parameters).
            If the absolute path is empty, use a forward slash character (/).

        CanonicalQueryString -
            The URL-encoded query string parameters, separated by ampersands (&). Percent-encode reserved characters,
            including the space character. Encode names and values separately.
            If there are empty parameters, append the equals sign to the parameter name before encoding.
            After encoding, sort the parameters alphabetically by key name.
            If there is no query string, use an empty string ("").

        CanonicalHeaders -
            The request headers, that will be signed, and their values, separated by newline characters.
            Header names must use lowercase characters, must appear in alphabetical order,
            and must be followed by a colon (:). For the values, trim any leading or trailing spaces,
            convert sequential spaces to a single space, and separate the values for a multi-value header using commas.
            You must include the host header (HTTP/1.1) or the :authority header (HTTP/2),
            and any x-amz-* headers in the signature.
            You can optionally include other standard headers in the signature, such as content-type.

        SignedHeaders -
            The list of headers that you included in CanonicalHeaders, separated by semicolons (;).
            This indicates which headers are part of the signing process.
            Header names must use lowercase characters and must appear in alphabetical order.

        HashedPayload -
            A string created using the payload in the body of the HTTP request as input to a hash function.
            This string uses lowercase hexadecimal characters. If the payload is empty,
            use an empty string as the input to the hash function.
        """
        canonical_headers, signed_headers = _generate_canonical_headers(headers)
        canonical_query_string = _generate_canonical_query_string(url.query)

        path = _quote(url.path or "/")
        # CanonicalRequest =
        #   HTTPRequestMethod + '\n' +
        #   CanonicalURI + '\n' +
        #   CanonicalQueryString + '\n' +
        #   CanonicalHeaders + '\n\n' +
        #   SignedHeaders + '\n' +
        canonical_request = (
            f"{method}\n"
            f"{path}\n"
            f"{canonical_query_string}\n"
            f"{canonical_headers}\n\n"
            f"{signed_headers}\n"
            f"{content_sha256}"
        )
        logger.debug(f"canonical_request: {canonical_request}")

        return sha256_hash(canonical_request), signed_headers

    @staticmethod
    def _generate_authorization(
        auth_type: str,
        access_key: str,
        scope: str,
        signed_headers: str,
        signature: typing.Union[str, bytes],
    ) -> str:
        """Get authorization."""
        return f"{auth_type} Credential={access_key}/{scope}, SignedHeaders={signed_headers}, Signature={signature}"

    def sign_v4(
        self,
        service_name: str,
        method: str,
        url: httpx.URL,
        partition: str,
        headers: multidict.CIMultiDict,
        credentials: KeyPair,
        content: typing.Union[bytes, None],
        date: datetime,
    ) -> multidict.CIMultiDict:
        logger.debug(f"url: {url}")
        logger.debug(f"headers: {headers}")
        content_sha256 = sha256_hash(content) if url.scheme == "http" else "UNSIGNED-PAYLOAD"
        content_header = f"{self.header_prefix}-content-sha256"
        if content_header not in headers:
            headers[content_header] = content_sha256
        scope = self._generate_scope(self.auth_schema, date, partition, service_name)
        canonical_request_hash, signed_headers = self._generate_canonical_request_hash(
            method,
            url,
            headers,
            content_sha256,
        )
        string_to_sign = self._generate_string_to_sign(self.auth_type, date, scope, canonical_request_hash)
        logger.debug(f"scope: {scope}")
        logger.debug(f"string_to_sign: {string_to_sign}")
        signing_key = _generate_signing_key(
            self.auth_schema,
            credentials.secret_access_key,
            to_signer_date(date),
            partition,
            service_name,
        )
        signature = _generate_signature(signing_key, string_to_sign)
        authorization = self._generate_authorization(
            self.auth_type,
            credentials.access_key_id,
            scope,
            signed_headers,
            signature,
        )
        headers["Authorization"] = authorization
        return headers


class Validator:
    @staticmethod
    def _parse_authorization(authorization: str) -> typing.Tuple[str, str, str, str]:
        auth_type, _, credentials = authorization.partition(" ")
        parts = credentials.split(", ")
        data = {}
        for part in parts:
            k, _, v = part.partition("=")
            data[k.lower()] = v

        return auth_type, data["credential"], data["signedheaders"], data["signature"]

    @staticmethod
    def _parse_credential(credential: str) -> typing.Tuple[str, str]:
        return tuple(credential.split("/", maxsplit=1))

    @staticmethod
    def _parse_scope(scope: str) -> typing.Tuple[str, str, str]:
        """Convert a date/partition/service_name/request_tyep scope into a (date, partition, service_name) tuple."""
        return tuple(scope.split("/")[:-1])

    @staticmethod
    def _parse_key_date(headers: multidict.CIMultiDict) -> str:
        """Convert a date/partition/service_name/request_tyep scope into a (date, partition, service_name) tuple."""
        key_date = headers.get("x-amz-date", headers.get("x-neos-date"))
        if key_date is None:
            msg = "Missing supported date header"
            raise error.SignatureError(msg)
        # TODO: detect drift/replay

        return key_date

    @staticmethod
    def _generate_canonical_request_hash(
        method: str,
        url: httpx.URL,
        headers: multidict.CIMultiDict,
        signed_headers: str,
        content_sha256: str,
    ) -> str:
        """Get canonical request hash."""
        canonical_headers = _recreate_canonical_headers(headers, signed_headers)
        canonical_query_string = _generate_canonical_query_string(url.query)

        path = _quote(url.path or "/")
        # CanonicalRequest =
        #   HTTPRequestMethod + '\n' +
        #   CanonicalURI + '\n' +
        #   CanonicalQueryString + '\n' +
        #   CanonicalHeaders + '\n\n' +
        #   SignedHeaders + '\n' +
        #   HexEncode(Hash(RequestPayload))  noqa: ERA001
        canonical_request = (
            f"{method}\n"
            f"{path}\n"
            f"{canonical_query_string}\n"
            f"{canonical_headers}\n\n"
            f"{signed_headers}\n"
            f"{content_sha256}"
        )
        logger.debug(f"challenge canonical_request: {canonical_request}")
        return sha256_hash(canonical_request)

    @staticmethod
    def _generate_string_to_sign(auth_type: str, date: str, scope: str, canonical_request_hash: str) -> str:
        """Get string-to-sign."""
        return f"{auth_type}\n{date}\n{scope}\n{canonical_request_hash}"

    def challenge_v4(
        self,
        method: str,
        url: httpx.URL,
        headers: multidict.CIMultiDict,
        content: typing.Tuple[bytes, None],
    ) -> typing.Tuple[str, str, str, str, str]:
        logger.debug(f"url: {url}")
        logger.debug(f"headers: {headers}")
        auth_type, credential, signed_headers, signature = self._parse_authorization(headers["Authorization"])

        auth_schema = auth_type.split("-")[0]
        header_prefix = "x-neos" if auth_schema == "NEOS4" else "x-amz"
        content_header = f"{header_prefix}-content-sha256"
        content_sha256 = (
            sha256_hash(content)
            if headers.get(content_header, "UNSIGNED-PAYLOAD") != "UNSIGNED-PAYLOAD"
            else "UNSIGNED-PAYLOAD"
        )

        access_key, scope = self._parse_credential(credential)
        date, partition, service_name = self._parse_scope(scope)
        key_date = self._parse_key_date(headers)

        canonical_request_hash = self._generate_canonical_request_hash(
            method,
            url,
            headers,
            signed_headers,
            content_sha256,
        )
        string_to_sign = self._generate_string_to_sign(auth_type, key_date, scope, canonical_request_hash)
        logger.debug(f"challenge scope: {scope}")
        logger.debug(f"challenge string_to_sign: {string_to_sign}")

        return auth_type, access_key, scope, string_to_sign, signature

    def validate_challenge(
        self,
        auth_schema: str,
        scope: str,
        string_to_sign: str,
        signature: str,
        secret_key: str,
    ) -> bool:
        date, partition, service_name = self._parse_scope(scope)
        signing_key = _generate_signing_key(
            auth_schema,
            secret_key,
            date,
            partition,
            service_name,
        )
        signature_ = _generate_signature(signing_key, string_to_sign)

        if signature_ != signature:
            logger.info(f"Provided signature: {signature}, Calculated signature: {signature_}")
            msg = "Invalid signature"
            raise error.SignatureError(msg)

        return True
