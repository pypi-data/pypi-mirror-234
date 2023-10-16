#  Copyright (c) 2023 Roboto Technologies, Inc.
import datetime
import enum
import typing

import pydantic


class CollectionResourceType(str, enum.Enum):
    Dataset = "dataset"


class CollectionContentMode(str, enum.Enum):
    SummaryOnly = "summary_only"
    References = "references"
    Full = "full"


class CollectionResourceRef(pydantic.BaseModel):
    resource_type: CollectionResourceType
    resource_id: str
    resource_version: typing.Optional[str] = None


class CollectionRecord(pydantic.BaseModel):
    collection_id: str
    name: typing.Optional[str] = None
    description: typing.Optional[str] = None
    resources: dict[CollectionResourceType, list[typing.Any]] = pydantic.Field(
        default_factory=dict
    )
    missing: dict[CollectionResourceType, list[CollectionResourceRef]] = pydantic.Field(
        default_factory=dict
    )
    tags: list[str] = []
    version: int
    created: datetime.datetime
    created_by: str
    updated: datetime.datetime
    updated_by: str
    org_id: str


class CollectionChangeSet(pydantic.BaseModel):
    added_resources: list[CollectionResourceRef] = pydantic.Field(default_factory=list)
    added_tags: list[str] = pydantic.Field(default_factory=list)
    removed_resources: list[CollectionResourceRef] = pydantic.Field(
        default_factory=list
    )
    removed_tags: list[str] = pydantic.Field(default_factory=list)
    field_changes: dict[str, typing.Any] = pydantic.Field(default_factory=list)


class CollectionChangeRecord(pydantic.BaseModel):
    collection_id: str
    from_version: int
    to_version: int
    change_set: CollectionChangeSet
    applied: datetime.datetime
    applied_by: str
