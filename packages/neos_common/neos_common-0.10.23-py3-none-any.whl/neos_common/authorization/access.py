import logging
import typing
from collections import defaultdict

from neos_common import base, schema
from neos_common.base import ResourceLike, ResourceReader

logger = logging.getLogger(__name__)


STAR = "*"


"""
+--------+-----------------------+----------------------+---------+
| case # | statement resource_id | endpoint resource_id | outcome |
+--------+-----------------------+----------------------+---------+
|     33 | exact                 | exact                | allow   |
|     32 | exact                 | *                    | allow   |
|     31 | exact                 | null                 | deny    |
|     23 | *                     | exact                | allow   |
|     22 | *                     | *                    | allow   |
|     21 | *                     | null                 | deny    |
|     13 | null                  | exact                | deny    |
|     12 | null                  | *                    | deny    |
|     11 | null                  | null                 | allow   |
+--------+-----------------------+----------------------+---------+

TODO: rethink the case 12 with product owners
    UPDATE: case 32 deny -> allow (to support listing of data products which are allowed for user to see)
"""

_ACCESS_MAP = {
    "33": True,
    "32": True,
    "23": True,
    "22": True,
    "11": True,
}


def _map_resource_id(resource_id: typing.Union[str, None]) -> str:
    ret = 3
    if resource_id is None:
        ret = 1
    elif resource_id == STAR:
        ret = 2
    return str(ret)


def check_resource(statement: schema.Statement, resource: ResourceLike) -> bool:
    checks: typing.List[bool] = []
    if not statement.resource:
        return False

    if resource.all_:
        return True

    for statement_resource_str in statement.resource:
        # Allow all resources if *
        if statement_resource_str == STAR:
            checks.append(True)
            continue

        # Validate *rn string
        statement_resource = resource.parse(statement_resource_str)

        # Exact match of the prefix parts
        prefix_check = all(
            [
                resource.partition == statement_resource.partition,
                resource.service == statement_resource.service,
                resource.identifier == statement_resource.identifier,
                (resource.account_id == statement_resource.account_id or statement_resource.account_id == "root"),
                resource.resource_type == statement_resource.resource_type,
            ],
        )

        access_case = f"{_map_resource_id(statement_resource.resource_id)}{_map_resource_id(resource.resource_id)}"
        postfix_check = _ACCESS_MAP.get(access_case, False)

        # Exacts must be equal to pass
        if access_case == "33" and statement_resource.resource_id != resource.resource_id:
            postfix_check = False

        checks.append(all([prefix_check, postfix_check]))

    return any(checks)


def _intersect_principals(statement: schema.Statement, principal_ids: typing.List[str]) -> typing.List[str]:
    statement_principals = {
        str(p) for p in (statement.principal if isinstance(statement.principal, list) else [statement.principal])
    }
    intersect: typing.List[str] = list(set(principal_ids).intersection(statement_principals))
    return intersect


def check_principals_in_statement(
    statement: schema.Statement,
    principals: typing.Union[schema.Principals, typing.List[str]],
) -> bool:
    """Check intersection of principal_id in principals and statement.principal list."""
    principal_ids = principals.get_principal_ids() if isinstance(principals, schema.Principals) else principals

    principal_intersection = _intersect_principals(statement, principal_ids)
    return len(principal_intersection) > 0


def get_statement_priority(
    statement: schema.Statement,
    principals: typing.Union[schema.Principals, typing.List[str]],
) -> int:
    """Determine priority.

    Biggest priority wins.

      - User is stronger than group.
      - Deny is stronger than allow.


    No priority_type        -> priority 1
    Group priority_type     -> priority 10
    User priority_type      -> priority 20
    Deny effect             -> priority +5

    Renders to
    +----------------+--------+----------+
    | principal_type | effect | priority |
    +----------------+--------+----------+
    | none           | allow  |        1 |
    | none           | deny   |        6 |
    | group          | allow  |       10 |
    | group          | deny   |       15 |
    | user           | allow  |       20 |
    | user           | deny   |       25 |
    +----------------+--------+----------+
    """
    # Priority maps
    effect_bonus = 0
    if statement.effect == base.EffectEnum.deny.value:
        effect_bonus = 5

    if not isinstance(principals, schema.Principals):
        return 1 + effect_bonus

    principal_type_priority_map = {
        schema.PrincipalType.user: 20,
        schema.PrincipalType.group: 10,
    }

    # Determine principals priority
    principals_priority = {p.principal_id: principal_type_priority_map[p.principal_type] for p in principals.principals}

    # Determine statement principals priority
    principal_ids = principals.get_principal_ids()
    principal_intersection = _intersect_principals(statement, principal_ids)

    principal_intersection_priority = [
        principals_priority[principal_id] + effect_bonus for principal_id in principal_intersection
    ]

    return sorted(principal_intersection_priority).pop()


def filter_by_principals(
    statements: schema.Statements,
    principals: typing.Union[schema.Principals, typing.List[str]],
) -> schema.Statements:
    """Filter out those principals which are not statements."""
    filtered_statements = [
        statement.model_dump()
        for statement in statements.statements
        if check_principals_in_statement(statement, principals)
    ]

    return schema.Statements(statements=filtered_statements)


def filter_by_action(
    statements: schema.Statements,
    action: typing.Union[base.Action, str],
) -> schema.Statements:
    """Filter out those which are not * or don't match action."""
    filtered_statements = []
    for statement in statements.statements:
        action_str: str = action.value if isinstance(action, base.Action) else action
        if action_str in statement.action or STAR in statement.action:
            filtered_statements.append(statement.model_dump())

    return schema.Statements(statements=filtered_statements)


def filter_by_resource(
    statements: schema.Statements,
    resource: ResourceLike,
) -> schema.Statements:
    """Filter out those which don't pass check_resource()."""
    filtered_statements = [
        statement.model_dump() for statement in statements.statements if check_resource(statement, resource)
    ]

    return schema.Statements(statements=filtered_statements)


def order_by_priority_ascending(
    statements: schema.Statements,
    principals: typing.Union[schema.Principals, typing.List[str]],
) -> schema.PriorityStatements:
    """Order ascending statements by priority."""
    priority_statements = []
    for statement in statements.statements:
        priority = get_statement_priority(statement, principals)
        priority_statement = schema.PriorityStatement(priority=priority, **statement.model_dump())
        priority_statements.append(priority_statement)

    priority_statements.sort(key=lambda s: s.priority)

    return schema.PriorityStatements(statements=priority_statements)


def get_effect_by_resource_ids(
    statements: schema.Statements,
    principals: typing.Union[schema.Principals, typing.List[str]],
) -> typing.Dict[str, base.EffectEnum]:
    """Get allow/deny effect for resource ids by priority algo."""
    # Group all statements by resource_id
    statements_groupped_by_resource_id = defaultdict(list)
    for statement in statements.statements:
        for r in statement.resource:
            resource_from_iam = ResourceReader.parse(r)
            statements_groupped_by_resource_id[resource_from_iam.resource_id].append(statement)

    # Check if there is at least one allow statement for each resource_id
    allowed_resource_ids = {
        resource_id: base.EffectEnum.allow.value for resource_id in statements_groupped_by_resource_id
    }

    for resource_id in statements_groupped_by_resource_id:
        ordered_priority_statements = order_by_priority_ascending(
            schema.Statements(statements=statements_groupped_by_resource_id[resource_id]),
            principals,
        )

        if not ordered_priority_statements.statements[-1].is_allowed():
            allowed_resource_ids[resource_id] = base.EffectEnum.deny.value  # If biggest priority is deny, then deny

    return allowed_resource_ids
