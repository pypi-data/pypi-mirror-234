#  Copyright (c) 2023 Roboto Technologies, Inc.

import collections.abc
from typing import Optional, Union

from roboto.query import QuerySpecification
from roboto.sentinels import NotSet, NotSetType

from .collection_delegate import (
    CollectionDelegate,
)
from .collection_record import (
    CollectionChangeRecord,
    CollectionContentMode,
    CollectionRecord,
    CollectionResourceRef,
)


class Collection:
    __record: CollectionRecord
    __delegate: CollectionDelegate

    def __init__(self, delegate: CollectionDelegate, record: CollectionRecord):
        super().__init__()
        self.__record = record
        self.__delegate = delegate

    @classmethod
    def from_id(
        cls,
        collection_id: str,
        delegate: CollectionDelegate,
        org_id: Optional[str] = None,
        version: Optional[int] = None,
        content_mode: CollectionContentMode = CollectionContentMode.Full,
    ) -> "Collection":
        record = delegate.get_collection(
            collection_id=collection_id,
            org_id=org_id,
            version=version,
            content_mode=content_mode,
        )
        return cls(record=record, delegate=delegate)

    @classmethod
    def create(
        cls,
        delegate: CollectionDelegate,
        name: Optional[str] = None,
        description: Optional[str] = None,
        tags: Optional[list[str]] = None,
        resources: Optional[list[CollectionResourceRef]] = None,
        created_by: Optional[str] = None,
        org_id: Optional[str] = None,
    ) -> "Collection":
        record = delegate.create_collection(
            name=name,
            description=description,
            tags=tags,
            resources=resources,
            created_by=created_by,
            org_id=org_id,
        )
        return cls(record=record, delegate=delegate)

    @classmethod
    def list_all(
        cls,
        delegate: CollectionDelegate,
        org_id: Optional[str] = None,
        content_mode: CollectionContentMode = CollectionContentMode.SummaryOnly,
    ) -> collections.abc.Generator["Collection", None, None]:
        query = QuerySpecification()
        paginated_result = delegate.search_collections(
            query=query, org_id=org_id, content_mode=content_mode
        )

        while True:
            for record in paginated_result.items:
                yield cls(record=record, delegate=delegate)
            if paginated_result.next_token:
                query.after = paginated_result.next_token
                paginated_result = delegate.search_collections(
                    query=query, org_id=org_id, content_mode=content_mode
                )
            else:
                break

    def changes(
        self, from_version: Optional[int] = None, to_version: Optional[int] = None
    ) -> collections.abc.Generator["CollectionChangeRecord", None, None]:
        paginated_results = self.__delegate.get_collection_changes(
            collection_id=self.__record.collection_id,
            org_id=self.__record.org_id,
            from_version=from_version,
            to_version=to_version,
        )

        while True:
            for record in paginated_results.items:
                yield record
            if paginated_results.next_token:
                paginated_results = self.__delegate.get_collection_changes(
                    collection_id=self.__record.collection_id,
                    org_id=self.__record.org_id,
                    from_version=from_version,
                    to_version=to_version,
                    page_token=paginated_results.next_token,
                )
            else:
                break

    def delete(self):
        self.__delegate.delete_collection(
            collection_id=self.__record.collection_id, org_id=self.__record.org_id
        )

    def update(
        self,
        name: Optional[Union[NotSetType, str]] = NotSet,
        description: Optional[Union[NotSetType, str]] = NotSet,
        add_resources: Union[NotSetType, list[CollectionResourceRef]] = NotSet,
        remove_resources: Union[NotSetType, list[CollectionResourceRef]] = NotSet,
        add_tags: Union[NotSetType, list[str]] = NotSet,
        remove_tags: Union[NotSetType, list[str]] = NotSet,
        updated_by: Optional[str] = None,
    ) -> "Collection":
        self.__record = self.__delegate.update_collection(
            collection_id=self.__record.collection_id,
            name=name,
            description=description,
            add_resources=add_resources,
            remove_resources=remove_resources,
            add_tags=add_tags,
            remove_tags=remove_tags,
            updated_by=updated_by,
            org_id=self.__record.org_id,
        )

        return self

    @property
    def record(self) -> CollectionRecord:
        return self.__record
