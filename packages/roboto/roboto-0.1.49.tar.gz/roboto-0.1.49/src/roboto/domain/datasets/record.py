#  Copyright (c) 2023 Roboto Technologies, Inc.

import datetime
import enum
from typing import Any, Optional

import pydantic


class Administrator(str, enum.Enum):
    # Other supported type would be "Customer"
    Roboto = "Roboto"


class StorageLocation(str, enum.Enum):
    # Other supported locations might be "GCP" or "Azure"
    S3 = "S3"


# https://www.google.com/search?q=pydantic.Field+default_factory+not+evaluated+in+parse_obj&rlz=1C5CHFA_enUS1054US1054&oq=pydantic.Field+default_factory+not+evaluated+in+parse_obj&aqs=chrome..69i57j33i160.6235j0j7&sourceid=chrome&ie=UTF-8
class DatasetRecord(pydantic.BaseModel):
    # Primary key, defined in CDK
    org_id: str  # partition key
    dataset_id: str  # sort key

    administrator: Administrator
    # Persisted as ISO 8601 string in UTC
    created: datetime.datetime
    created_by: str
    description: Optional[str]
    metadata: dict[str, Any] = pydantic.Field(default_factory=dict)
    # Persisted as ISO 8601 string in UTC
    modified: datetime.datetime
    modified_by: str
    storage_location: StorageLocation
    tags: list[str] = pydantic.Field(default_factory=list)
    roboto_record_version: int = 0  # A protected field, incremented on every update
