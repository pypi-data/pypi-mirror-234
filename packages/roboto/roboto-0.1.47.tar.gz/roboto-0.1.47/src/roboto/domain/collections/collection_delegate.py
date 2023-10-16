#  Copyright (c) 2023 Roboto Technologies, Inc.
import abc
from typing import Optional, Union

from roboto.http import PaginatedList
from roboto.query import QuerySpecification
from roboto.sentinels import NotSet, NotSetType

from .collection_record import (
    CollectionChangeRecord,
    CollectionContentMode,
    CollectionRecord,
    CollectionResourceRef,
)


class CollectionDelegate(abc.ABC):
    @abc.abstractmethod
    def create_collection(
        self,
        name: Optional[str] = None,
        description: Optional[str] = None,
        resources: Optional[list[CollectionResourceRef]] = None,
        tags: Optional[list[str]] = None,
        created_by: Optional[str] = None,
        org_id: Optional[str] = None,
    ) -> CollectionRecord:
        raise NotImplementedError("create_collection")

    @abc.abstractmethod
    def get_collection(
        self,
        collection_id: str,
        org_id: Optional[str] = None,
        version: Optional[int] = None,
        content_mode: CollectionContentMode = CollectionContentMode.Full,
    ) -> CollectionRecord:
        raise NotImplementedError("get_collection")

    @abc.abstractmethod
    def get_collection_changes(
        self,
        collection_id: str,
        org_id: Optional[str] = None,
        from_version: Optional[int] = None,
        to_version: Optional[int] = None,
        page_token: Optional[str] = None,
    ) -> PaginatedList[CollectionChangeRecord]:
        raise NotImplementedError("get_collection_changes")

    @abc.abstractmethod
    def search_collections(
        self,
        query: QuerySpecification,
        org_id: Optional[str] = None,
        content_mode: CollectionContentMode = CollectionContentMode.SummaryOnly,
    ) -> PaginatedList[CollectionRecord]:
        raise NotImplementedError("search_collections")

    @abc.abstractmethod
    def update_collection(
        self,
        collection_id: str,
        name: Optional[Union[NotSetType, str]] = NotSet,
        description: Optional[Union[NotSetType, str]] = NotSet,
        add_resources: Union[NotSetType, list[CollectionResourceRef]] = NotSet,
        remove_resources: Union[NotSetType, list[CollectionResourceRef]] = NotSet,
        add_tags: Union[NotSetType, list[str]] = NotSet,
        remove_tags: Union[NotSetType, list[str]] = NotSet,
        updated_by: Optional[str] = None,
        org_id: Optional[str] = None,
    ) -> CollectionRecord:
        raise NotImplementedError("update_collection")

    @abc.abstractmethod
    def delete_collection(
        self,
        collection_id: str,
        org_id: Optional[str] = None,
    ):
        raise NotImplementedError("delete_collection")
