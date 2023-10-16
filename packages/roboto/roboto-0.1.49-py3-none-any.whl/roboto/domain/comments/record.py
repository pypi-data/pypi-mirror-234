#  Copyright (c) 2023 Roboto Technologies, Inc.

import datetime
from enum import Enum

import pydantic


class EntityType(str, Enum):
    Action = "action"
    Collection = "collection"
    Dataset = "dataset"
    File = "file"
    Invocation = "invocation"
    Trigger = "trigger"


class CommentRecord(pydantic.BaseModel):
    # Primary key, defined in CDK
    org_id: str  # partition key
    comment_id: str
    entity_type: EntityType
    entity_id: str
    # Persisted as ISO 8601 string in UTC
    created: datetime.datetime
    created_by: str
    comment_text: str
    mentions: list[str] = pydantic.Field(default_factory=list)
    # Persisted as ISO 8601 string in UTC
    modified: datetime.datetime
    modified_by: str

    # for v2
    # parent_comment_id: str
