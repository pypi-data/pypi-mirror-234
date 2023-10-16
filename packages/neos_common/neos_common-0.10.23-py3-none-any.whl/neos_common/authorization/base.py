import typing
import uuid
from dataclasses import dataclass

import fastapi

from neos_common.authorization.token import TokenData
from neos_common.base import Action, ApiConfig, Config, ResourceLike, ResourceType
from neos_common.client import IAMClient, KeycloakClient


class SignatureValidator(typing.Protocol):
    """Define the base requirements for an object that can validate signed requests."""

    async def validate(
        self,
        request: "fastapi.Request",
        action: typing.List[typing.Union[Action, str]],
        resource: typing.List[ResourceLike],
        *,
        return_allowed_resources: bool,
    ) -> typing.Tuple[uuid.UUID, typing.List[str]]:
        """Validate a request and return the associated user_id and resources."""
        ...  # pragma: no cover


class AccessValidator:
    async def validate(
        self,
        user_id: uuid.UUID,
        actions: typing.List[typing.Union[Action, str]],
        resources: typing.List[ResourceLike],
        *,
        return_allowed_resources: bool = True,
    ) -> typing.Tuple[uuid.UUID, typing.List[str]]:
        ...  # pragma: no cover


class ConfigDependency(typing.Protocol):
    """Define the base requirements for a dependency that returns Config."""

    async def __call__(self, request: "fastapi.Request") -> Config:
        ...  # pragma: no cover


class SignatureValidatorDependency(typing.Protocol):
    """Define the base requirements for a dependency that returns a SignatureValidator."""

    async def __call__(self) -> SignatureValidator:
        ...  # pragma: no cover


class IAMClientDependency(typing.Protocol):
    """Define the base requirements for a dependency that returns an IAMClient."""

    async def __call__(self, config: Config) -> IAMClient:
        ...  # pragma: no cover


class AccessValidatorDependency(typing.Protocol):
    """Define the base requirements for a dependency that returns an AccessValidator."""

    async def __call__(self, iam_client: IAMClient, token: TokenData) -> AccessValidator:
        ...  # pragma: no cover


class KeycloakClientDependency(typing.Protocol):
    """Define the base requirements for a dependency that returns a KeycloakClient."""

    async def __call__(self, config: ApiConfig) -> KeycloakClient:
        ...  # pragma: no cover


@dataclass
class ActionResource:
    action: Action
    resource_type: ResourceType
    resource: ResourceLike
    resource_extractor: typing.Union[typing.Callable[[fastapi.Request], typing.Dict[str, str]], None] = None


class AuthorizationDependency(typing.Protocol):
    """Define the base requirements for a dependency that validates authorization."""

    def __init__(
        self,
        action_resources: typing.Union[typing.List[ActionResource], ActionResource],
        *,
        return_allowed_resources: bool = False,
    ) -> None:
        ...  # pragma: no cover

    async def __call__(
        self,
        request: fastapi.Request,
        keycloak_client: KeycloakClient,
        config: Config,
        signature_validator: SignatureValidator,
        access_validator: AccessValidator,
    ) -> TokenData:
        ...  # pragma: no cover
