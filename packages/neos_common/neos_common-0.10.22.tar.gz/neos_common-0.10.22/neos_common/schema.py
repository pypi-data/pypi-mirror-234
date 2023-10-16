import enum
import typing
from uuid import UUID

import pydantic

from neos_common import base

ResourcePattern = pydantic.constr(pattern=base.ResourceBase.RESOURCE_PATTERN)


class Statement(pydantic.BaseModel):
    model_config = pydantic.ConfigDict(use_enum_values=True)

    sid: str
    principal: typing.Union[typing.List[str], UUID]
    action: typing.List[str]
    resource: typing.List[ResourcePattern]  # type: ignore[reportGeneralTypeIssues]
    condition: typing.List[str] = pydantic.Field(default_factory=list)
    effect: base.EffectEnum

    def is_allowed(self) -> bool:
        return self.effect == base.EffectEnum.allow.value


class PriorityStatement(Statement):
    priority: int


class Statements(pydantic.BaseModel):
    statements: typing.List[Statement]


class PriorityStatements(pydantic.BaseModel):
    statements: typing.List[PriorityStatement]


class SocketRequest(pydantic.BaseModel):
    request_type: str
    data: typing.Dict[str, typing.Any]


class PrincipalType(enum.Enum):
    model_config = pydantic.ConfigDict(use_enum_values=True)

    user = "user"
    group = "group"


class Principal(pydantic.BaseModel):
    principal_id: str
    principal_type: PrincipalType


class Principals(pydantic.BaseModel):
    principals: typing.List[Principal]

    def get_principal_ids(self) -> typing.List[str]:
        return [p.principal_id for p in self.principals]


class EventPacket(pydantic.BaseModel):
    source: str
    timestamp: int  # timestamp in ms
    span_id: pydantic.UUID4
    version: str
    message: typing.Union[str, typing.Dict[str, typing.Any]]
    message_type: str

    @pydantic.field_validator("span_id")
    def span_id_to_str(cls, value: pydantic.UUID4) -> str:
        return str(value)


class EventPackets(pydantic.BaseModel):
    packets: typing.List[EventPacket]
