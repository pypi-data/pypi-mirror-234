import logging
import typing

from neos_common.authorization.signer import KeyPair
from neos_common.client.base import NeosClient

if typing.TYPE_CHECKING:
    from neos_common.authorization.token import TokenData

logger = logging.getLogger(__name__)


class RegistryClient(NeosClient):
    known_errors: typing.ClassVar[typing.Set[str]] = {
        "R100",
        "R101",
        "R110",
        "R111",
        "R112",
        "R113",
        "R114",
        "R115",
        "A200",
        "A201",
    }

    def __init__(
        self,
        host: str,
        token: "typing.Union[TokenData, None]",
        key_pair: typing.Union[KeyPair, None],
        account: str,
        partition: str,
    ) -> None:
        assert token is not None or key_pair is not None

        self._token = token
        self._key_pair = key_pair

        self._account = account
        self._partition = partition

        self._host = host
        self._principals = None

    @property
    def service_name(self) -> str:
        return "Registry"

    @property
    def token(self) -> "typing.Union[TokenData, None]":
        return self._token

    @property
    def key_pair(self) -> typing.Union[KeyPair, None]:
        return self._key_pair

    @property
    def core_url(self) -> str:
        return f"{self._host}/core/{{identifier}}/announce"

    @property
    def data_product_url(self) -> str:
        return f"{self._host}/core/{{identifier}}/data_product"

    @property
    def metadata_url(self) -> str:
        return f"{self._host}/core/{{identifier}}/data_product/metadata"

    async def announce_core(self, host: str, version: str, core_identifier: str) -> None:
        r = await self._post(
            url=self.core_url.format(identifier=core_identifier),
            json={
                "host": host,
                "version": version,
            },
            headers={"X-Account": self._account, "X-Partition": self._partition},
        )

        self.process_response(r)

    async def register_data_product(
        self,
        urn: str,
        name: str,
        metadata: dict,
        description: str,
        sanitized_name: str,
        data_product_type: str,
        engine: str,
        table: str,
        identifier: str,
        core_identifier: str,
        *,
        public: bool = True,
    ) -> None:
        json = {
            "urn": urn,
            "name": name,
            "metadata": metadata,
            "description": description,
            "sanitized_name": sanitized_name,
            "data_product_type": data_product_type,
            "engine": engine,
            "table": table,
            "identifier": identifier,
            "public": public,
        }
        logger.info(
            f"Register data product request: {json}",
        )

        r = await self._post(
            url=self.data_product_url.format(identifier=core_identifier),
            json=json,
            headers={"X-Account": self._account, "X-Partition": self._partition},
        )

        self.process_response(r)

    async def update_data_product_metadata(
        self,
        urn: str,
        metadata: dict,
        description: str,
        core_identifier: str,
    ) -> None:
        r = await self._post(
            url=self.metadata_url.format(identifier=core_identifier),
            json={
                "urn": urn,
                "metadata": metadata,
                "description": description,
            },
            headers={"X-Account": self._account, "X-Partition": self._partition},
        )

        self.process_response(r)

    async def deregister_data_product(self, urn: str, core_identifier: str) -> None:
        r = await self._delete(
            url=self.data_product_url.format(identifier=core_identifier),
            json={
                "urn": urn,
            },
            headers={"X-Account": self._account, "X-Partition": self._partition},
        )

        self.process_response(r)
