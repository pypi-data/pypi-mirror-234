import collections.abc
import datetime
import enum
import hashlib
import json
import typing

import pydantic

from ...serde import pydantic_jsonable_dict
from .action_container_resources import (
    ComputeRequirements,
    ContainerParameters,
)


class Accessibility(str, enum.Enum):
    """
    Controls who can query for and invoke an action.

    Future accessibility levels may include: "user" and/or "team".
    """

    Organization = "organization"
    """All members of the organization owning the Action can query for and invoke the action."""

    ActionHub = "action_hub"
    """All users of Roboto can query for and invoke the action."""


class ActionParameter(pydantic.BaseModel):
    name: str
    required: bool = False
    description: typing.Optional[str] = None
    default: typing.Optional[typing.Any] = None

    def __eq__(self, other: typing.Any) -> bool:
        if not isinstance(other, ActionParameter):
            return NotImplemented

        return (
            self.name == other.name
            and self.required == other.required
            and self.description == other.description
            and self.default == other.default
        )

    class Config:
        extra = "forbid"


class ActionParameterChangeset(pydantic.BaseModel):
    put_parameters: list[ActionParameter] = pydantic.Field(default_factory=list)
    remove_parameters: list[str] = pydantic.Field(default_factory=list)

    class Builder:
        __put_parameters: list[ActionParameter]
        __remove_parameters: list[str]

        def __init__(self) -> None:
            self.__put_parameters = []
            self.__remove_parameters = []

        def put_parameter(
            self, parameter: ActionParameter
        ) -> "ActionParameterChangeset.Builder":
            self.__put_parameters.append(parameter)
            return self

        def remove_parameter(
            self, parameter_name: str
        ) -> "ActionParameterChangeset.Builder":
            self.__remove_parameters.append(parameter_name)
            return self

        def build(self) -> "ActionParameterChangeset":
            changeset: collections.abc.Mapping = {
                "put_parameters": self.__put_parameters,
                "remove_parameters": self.__remove_parameters,
            }
            return ActionParameterChangeset(**{k: v for k, v in changeset.items() if v})

    def is_empty(self) -> bool:
        return not self.put_parameters and not self.remove_parameters


class ActionReference(pydantic.BaseModel):
    """Qualified action reference."""

    name: str
    digest: typing.Optional[str] = None
    owner: typing.Optional[str] = None

    def __eq__(self, other: typing.Any) -> bool:
        if not isinstance(other, ActionReference):
            return NotImplemented

        return (
            self.name == other.name
            and self.digest == other.digest
            and self.owner == other.owner
        )


class ActionRecord(pydantic.BaseModel):
    # Required fields without defaults
    created: datetime.datetime  # Persisted as ISO 8601 string in UTC
    created_by: str
    modified: datetime.datetime  # Persisted as ISO 8601 string in UTC
    modified_by: str
    name: str  # Sort key
    org_id: str  # Partition key

    # Optional fields with defaults
    accessibility: Accessibility = Accessibility.Organization
    compute_requirements: typing.Optional[ComputeRequirements] = None
    container_parameters: typing.Optional[ContainerParameters] = None
    description: typing.Optional[str] = None
    digest: typing.Optional[str] = None
    inherits: typing.Optional[ActionReference] = None
    metadata: dict[str, typing.Any] = pydantic.Field(default_factory=dict)
    parameters: list[ActionParameter] = pydantic.Field(default_factory=list)
    # Persisted as ISO 8601 string in UTC
    published: typing.Optional[datetime.datetime] = None
    tags: list[str] = pydantic.Field(default_factory=list)
    uri: typing.Optional[str] = None

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.digest = self.compute_digest() if not self.digest else self.digest

    def compute_digest(self) -> str:
        hasher = hashlib.blake2b(
            digest_size=16,
            # https://docs.python.org/3.9/library/hashlib.html#personalization
            person=b"ActionRecord",
        )
        digestable = pydantic_jsonable_dict(self, exclude_unset=True)
        hasher.update(json.dumps(digestable, sort_keys=True).encode("utf-8"))
        return hasher.hexdigest()

    @property
    def reference(self) -> ActionReference:
        return ActionReference(
            name=self.name,
            digest=self.digest,
            owner=self.org_id,
        )
