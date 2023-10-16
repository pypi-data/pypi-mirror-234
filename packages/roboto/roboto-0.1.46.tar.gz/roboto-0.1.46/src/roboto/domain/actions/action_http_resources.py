from typing import Any, Optional, Union

import pydantic

from ...sentinels import NotSet, NotSetType
from ...updates import MetadataChangeset
from .action_container_resources import (
    ComputeRequirements,
    ContainerParameters,
)
from .action_record import (
    Accessibility,
    ActionParameter,
    ActionParameterChangeset,
    ActionReference,
)


class CreateActionRequest(pydantic.BaseModel):
    # Required
    name: str

    # Optional
    parameters: Optional[list[ActionParameter]] = pydantic.Field(default_factory=list)
    description: Optional[str] = None
    uri: Optional[str] = None
    inherits: Optional[ActionReference] = None
    metadata: Optional[dict[str, Any]] = pydantic.Field(default_factory=dict)
    tags: Optional[list[str]] = pydantic.Field(default_factory=list)
    compute_requirements: Optional[ComputeRequirements] = None
    container_parameters: Optional[ContainerParameters] = None


class QueryActionsRequest(pydantic.BaseModel):
    filters: dict[str, Any] = pydantic.Field(default_factory=dict)

    class Config:
        extra = "forbid"


class SetActionAccessibilityRequest(pydantic.BaseModel):
    accessibility: Accessibility
    digest: Optional[str] = None
    """Specify specific version of Action. If not specified, the latest version's accessibility will be updated."""

    class Config:
        extra = "forbid"


class UpdateActionRequest(pydantic.BaseModel):
    compute_requirements: Union[ComputeRequirements, NotSetType] = NotSet
    container_parameters: Union[ContainerParameters, NotSetType] = NotSet
    description: Optional[Union[str, NotSetType]] = NotSet
    metadata_changeset: Union[MetadataChangeset, NotSetType] = NotSet
    parameter_changeset: Union[ActionParameterChangeset, NotSetType] = NotSet
    uri: Union[str, NotSetType] = NotSet

    @pydantic.validator("uri")
    def validate_uri(cls, v):
        if v is NotSet:
            return v

        stripped = v.strip()
        if not stripped:
            raise ValueError("uri cannot be empty")
        return stripped

    class Config:
        extra = "forbid"
        schema_extra = NotSetType.openapi_schema_modifier
