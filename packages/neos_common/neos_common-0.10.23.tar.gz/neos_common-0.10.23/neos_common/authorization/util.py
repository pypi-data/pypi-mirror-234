import logging
import typing

import fastapi
import keycloak
from fastapi.openapi.models import HTTPBearer as HTTPBearerModel
from fastapi.security.base import SecurityBase

from neos_common import base, error
from neos_common.authorization import token, validator
from neos_common.authorization.base import (
    AccessValidator,
    AccessValidatorDependency,
    ActionResource,
    AuthorizationDependency,
    ConfigDependency,
    IAMClientDependency,
    KeycloakClientDependency,
    SignatureValidator,
    SignatureValidatorDependency,
)
from neos_common.authorization.signer import KeyPair
from neos_common.base import ApiConfig, Config
from neos_common.client import IAMClient, KeycloakClient

logger = logging.getLogger(__name__)


def create_openapi_info(action: base.Action, resource: str) -> typing.Dict[str, str]:
    """Generate openapi info for use in FastAPI routes."""
    return {
        "x-iam-action": action.value,
        "x-iam-resource": resource,
    }


class DepKeycloakClientFactory:
    """Keycloak client dependency.

    Pull the config from the app.state, instantiate a keycloak client.

    Returns:
    -------
        KeycloakClient using configured keycloak parameters.
    """

    @classmethod
    def build(cls, config_dep: typing.Type[ConfigDependency]) -> typing.Type[KeycloakClientDependency]:
        """Build a KeycloakClientDependency.

        Generate a fastapi dependency that creates a KeycloakClient.
        """

        class DepKeycloakClient:
            async def __call__(self, config: ApiConfig = fastapi.Depends(config_dep())) -> KeycloakClient:
                return KeycloakClient(
                    host=config.keycloak_host,
                    realm=config.keycloak_realm,
                    client_id=config.keycloak_client_id,
                    client_secret=config.keycloak_client_secret,
                )

        return DepKeycloakClient


class DepAuthorizationFactory:
    """Authorization dependency.

    Pull the config from the app.state and parse the token from the request.

    Returns:
    -------
        TokenData with information about current user.
    """

    @classmethod
    def build(
        cls,
        config_dep: typing.Type[ConfigDependency],
        keycloak_dep: typing.Type[KeycloakClientDependency],
        signature_dep: typing.Type[SignatureValidatorDependency],
        access_validator: typing.Type[AccessValidatorDependency],
    ) -> typing.Type[AuthorizationDependency]:
        """Build an AuthorizationDependency.

        Generate a fastapi dependency that validates incoming authorization
        headers and creates TokenData.
        """

        class DepAuthorization(SecurityBase):
            def __init__(
                self,
                action_resources: typing.Union[typing.List[ActionResource], ActionResource],
                *,
                return_allowed_resources: bool = False,
            ) -> None:
                self.model = HTTPBearerModel()
                self.scheme_name = "bearer"

                self.action_resources = (
                    [action_resources] if isinstance(action_resources, ActionResource) else action_resources
                )
                self.return_allowed_resources = return_allowed_resources

            async def __call__(
                self,
                request: fastapi.Request,
                keycloak_client: KeycloakClient = fastapi.Depends(keycloak_dep()),
                config: Config = fastapi.Depends(config_dep()),
                signature_validator: SignatureValidator = fastapi.Depends(signature_dep()),
                access_validator: AccessValidator = fastapi.Depends(access_validator()),
            ) -> token.TokenData:
                authorization = request.headers.get("Authorization", "")
                auth_type, _, credentials = authorization.partition(" ")
                if auth_type == "":
                    msg = "Missing Authorization header."
                    raise error.AuthorizationRequiredError(msg)

                actions_: typing.List[typing.Union[base.Action, str]] = []
                resources_: typing.List[base.ResourceLike] = []

                for ar in self.action_resources:
                    resource_kwargs = ar.resource_extractor(request) if ar.resource_extractor else {"resource_id": None}
                    resources_.append(
                        ar.resource.generate_from_config(
                            config,
                            ar.resource_type,
                            **resource_kwargs,
                        ),
                    )
                    actions_.append(ar.action)

                if auth_type.lower() == "bearer":
                    access_token = credentials

                    logger.info(access_token)
                    try:
                        introspected_token = keycloak_client.introspect_token(access_token)
                    except keycloak.KeycloakError as e:
                        message = keycloak_client.parse_error(e)
                        logger.warning(message)
                        raise error.IdentityAccessManagerError(message) from e

                    if not introspected_token["active"]:
                        raise error.InvalidAuthorizationError

                    try:
                        user_id = introspected_token["sub"]
                    except KeyError as e:
                        msg = f"Invalid token format, {e!s}"
                        raise error.InvalidAuthorizationError(msg) from e

                    user_id, resources = (
                        await access_validator.validate(
                            user_id,
                            actions_,
                            resources_,
                            return_allowed_resources=self.return_allowed_resources,
                        )
                        if resources_ != []
                        else (user_id, [])
                    )

                    return token.TokenData(user_id, access_token, resources)

                if auth_type.lower() in ("neos4-hmac-sha256", "aws4-hmac-sha256"):
                    user_id, resources = await signature_validator.validate(
                        request,
                        actions_,
                        resources_,
                        return_allowed_resources=self.return_allowed_resources,
                    )
                    return token.TokenData(user_id=str(user_id), auth_token="none", resources=resources)  # nosec: B106

                msg = "Unsupported authorization header."
                raise error.InvalidAuthorizationError(msg)

        return DepAuthorization


class DepAccessValidatorFactory:
    """Access validator dependency."""

    @classmethod
    def build(
        cls,
        iam_client_dep: typing.Type[IAMClientDependency],
    ) -> typing.Type[AccessValidatorDependency]:
        """Build an AccessValidatorDependency.

        Generate a fastapi dependency that creates an AccessValidator.
        """

        class DepAccessValidator(AccessValidatorDependency):
            async def __call__(
                self,
                iam_client: IAMClient = fastapi.Depends(iam_client_dep()),
            ) -> validator.AccessValidator:
                return validator.AccessValidator(
                    iam_client=iam_client,
                )

        return DepAccessValidator


class DepIAMClientFactory:
    @classmethod
    def build(
        cls,
        config_dep: typing.Type[ConfigDependency],
    ) -> typing.Type[IAMClientDependency]:
        """Build an IAMClientDependency.

        Generate a fastapi dependency that creates an IAMClient.
        """

        class DepIAMClient:
            async def __call__(
                self,
                config: Config = fastapi.Depends(config_dep()),
            ) -> IAMClient:
                return IAMClient(
                    host=config.access_manager_host,  # type: ignore[reportGeneralTypeIssues]
                    token=None,
                    key_pair=KeyPair(
                        config.access_key_id,  # type: ignore[reportGeneralTypeIssues]
                        config.secret_access_key,  # type: ignore[reportGeneralTypeIssues]
                        config.partition,  # type: ignore[reportGeneralTypeIssues]
                    ),
                    account=config.account,  # type: ignore[reportGeneralTypeIssues]
                    partition=config.partition,  # type: ignore[reportGeneralTypeIssues]
                )

        return DepIAMClient
