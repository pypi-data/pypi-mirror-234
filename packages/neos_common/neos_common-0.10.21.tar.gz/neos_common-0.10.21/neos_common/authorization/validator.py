import logging
import typing
import uuid

import fastapi

from neos_common import error, schema
from neos_common.authorization import access, base, signer
from neos_common.authorization.access import STAR
from neos_common.base import Action, EffectEnum, ResourceLike
from neos_common.client import IAMClient

logger = logging.getLogger(__name__)


async def validate(
    action: typing.Union[Action, str],
    resource: ResourceLike,
    principals: typing.Union[schema.Principals, typing.List[str]],
    statements: schema.Statements,
    owner: typing.Union[str, None] = None,
) -> bool:
    """Validate access using PARC.

    Validate access (authorize) by checking PARC (principals, actions, resources, conditions) and
    effect (allow/deny) of endpoint requirements against statements stored in IAM.

    Statements adhear to priorities.

    User vs Group user type.
    User is stronger.
    +----------------+-----------------+-------------------+
    | user statement | group statement | validation result |
    +----------------+-----------------+-------------------+
    | deny           | deny            | deny              |
    | deny           | allow           | deny              |
    | allow          | deny            | allow             |
    | allow          | allow           | allow             |
    +----------------+-----------------+-------------------+

    Allow vs Deny effect.
    Deny is stronger.

    User type vs Effect.
    User type is stronger.
    """
    action_str: str = action.value if isinstance(action, Action) else action

    error_message = "The principal <{}> must have <{}> action for the resource <{}>.".format(
        owner or principals,
        action_str,
        resource.urn,
    )

    def raise_on_empty(statements: schema.Statements) -> None:
        if not statements.statements:
            raise error.InsufficientPermissionsError(error_message)

    filtered_statements = access.filter_by_principals(statements, principals)
    raise_on_empty(filtered_statements)

    filtered_statements = access.filter_by_action(filtered_statements, action)
    raise_on_empty(filtered_statements)

    filtered_statements = access.filter_by_resource(filtered_statements, resource)
    raise_on_empty(filtered_statements)

    effect_by_resource_ids = access.get_effect_by_resource_ids(filtered_statements, principals)

    # Explicit check
    if (
        effect_by_resource_ids.get(resource.resource_id) is not None
        and effect_by_resource_ids.get(resource.resource_id) == EffectEnum.deny.value
    ) and not (  # Explicit resource_id check
        resource.resource_id == STAR
        and STAR not in effect_by_resource_ids  # implicit wildcard * should not raise error
    ):
        raise error.InsufficientPermissionsError(error_message)

    # Implicit wildcard * check
    if resource.resource_id == STAR and not [
        rid for rid in effect_by_resource_ids.values() if rid == EffectEnum.allow.value
    ]:
        raise error.InsufficientPermissionsError(error_message)

    return True


class AccessValidator(base.AccessValidator):
    def __init__(self, iam_client: IAMClient) -> None:
        self._iam_client = iam_client

    async def validate(
        self,
        user_id: uuid.UUID,
        actions: typing.List[Action],
        resources: typing.List[ResourceLike],
        *,
        return_allowed_resources: bool = False,
    ) -> typing.Tuple[uuid.UUID, typing.List[str]]:
        return await self._iam_client.validate_token(
            principal=user_id,
            actions=actions,
            resources=[resource.urn for resource in resources],
            return_allowed_resources=return_allowed_resources,
        )


class SignatureValidator(base.SignatureValidator):
    def __init__(self, iam_client: IAMClient) -> None:
        self._iam_client = iam_client

    async def validate(
        self,
        request: fastapi.Request,
        actions: typing.List[Action],
        resources: typing.List[ResourceLike],
        *,
        return_allowed_resources: bool = False,
    ) -> typing.Tuple[uuid.UUID, typing.List[str]]:
        validator = signer.Validator()

        payload = await request.body()

        auth_type, access_key_id, scope, challenge, signature = validator.challenge_v4(
            request.method,
            request.url,
            request.headers,
            payload,
        )

        return await self._iam_client.validate_signature(
            access_key_id,
            auth_type.split("-")[0],
            scope,
            challenge,
            signature,
            actions,
            [resource.urn for resource in resources],
            return_allowed_resources=return_allowed_resources,
        )
