#  Copyright (c) 2023 Roboto Technologies, Inc.
import datetime
import enum
import typing

import pydantic

from ...pydantic import (
    validate_nonzero_gitpath_specs,
)
from ...query import ConditionType
from ..actions import (
    ActionReference,
    ComputeRequirements,
    ContainerParameters,
)


class TriggerForEachPrimitive(str, enum.Enum):
    Dataset = "dataset"
    DatasetFile = "dataset_file"


class TriggerRecord(pydantic.BaseModel):
    name: str  # Sort Key
    org_id: str  # Partition Key
    created: datetime.datetime  # Persisted as ISO 8601 string in UTC
    created_by: str
    modified: datetime.datetime  # Persisted as ISO 8601 string in UTC
    modified_by: str
    action: ActionReference
    required_inputs: list[str]
    for_each: TriggerForEachPrimitive = TriggerForEachPrimitive.Dataset
    enabled: bool = True
    parameter_values: dict[str, typing.Any] = pydantic.Field(default_factory=dict)
    additional_inputs: typing.Optional[list[str]] = None
    compute_requirement_overrides: typing.Optional[ComputeRequirements] = None
    container_parameter_overrides: typing.Optional[ContainerParameters] = None
    condition: typing.Optional[ConditionType] = None

    @pydantic.validator("required_inputs")
    def validate_required_inputs(cls, value: list[str]) -> list[str]:
        return validate_nonzero_gitpath_specs(value)

    @pydantic.validator("additional_inputs")
    def validate_additional_inputs(
        cls, value: typing.Optional[list[str]]
    ) -> typing.Optional[list[str]]:
        if value is None or len(value) == 0:
            return []

        return validate_nonzero_gitpath_specs(value)
