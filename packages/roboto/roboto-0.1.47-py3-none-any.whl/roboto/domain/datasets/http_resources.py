import typing

import pydantic

from ...updates import (
    MetadataChangeset,
    UpdateCondition,
)
from .record import Administrator, StorageLocation


class CreateDatasetRequest(pydantic.BaseModel):
    administrator: Administrator
    storage_location: StorageLocation
    description: typing.Optional[str]
    metadata: dict[str, typing.Any] = pydantic.Field(default_factory=dict)
    tags: list[str] = pydantic.Field(default_factory=list)


class QueryDatasetsRequest(pydantic.BaseModel):
    filters: dict[str, typing.Any] = pydantic.Field(default_factory=dict)

    class Config:
        extra = "forbid"


class UpdateDatasetRequest(pydantic.BaseModel):
    metadata_changeset: typing.Optional[MetadataChangeset] = None
    description: typing.Optional[str] = None
    conditions: typing.Optional[list[UpdateCondition]] = None
