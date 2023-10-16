#  Copyright (c) 2023 Roboto Technologies, Inc.
from typing import Optional, Union

import pydantic

from roboto.sentinels import NotSet, NotSetType

from .collection_record import (
    CollectionResourceRef,
)


class CreateCollectionRequest(pydantic.BaseModel):
    name: Optional[str]
    description: Optional[str]
    resources: Optional[list[CollectionResourceRef]]
    tags: Optional[list[str]]


class UpdateCollectionRequest(pydantic.BaseModel):
    name: Optional[Union[NotSetType, str]] = NotSet
    description: Optional[Union[NotSetType, str]] = NotSet
    add_resources: Union[list[CollectionResourceRef], NotSetType] = NotSet
    remove_resources: Union[list[CollectionResourceRef], NotSetType] = NotSet
    add_tags: Union[list[str], NotSetType] = NotSet
    remove_tags: Union[list[str], NotSetType] = NotSet

    class Config:
        schema_extra = NotSetType.openapi_schema_modifier
