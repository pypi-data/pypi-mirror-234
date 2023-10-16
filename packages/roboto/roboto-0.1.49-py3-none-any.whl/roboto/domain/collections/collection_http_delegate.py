#  Copyright (c) 2023 Roboto Technologies, Inc.
from typing import Any, Optional, Union
from urllib.parse import urlencode

from roboto.exceptions import (
    RobotoHttpExceptionParse,
)
from roboto.http import (
    HttpClient,
    PaginatedList,
    roboto_headers,
)
from roboto.query import QuerySpecification
from roboto.sentinels import NotSet, NotSetType
from roboto.serde import pydantic_jsonable_dict

from .collection_delegate import (
    CollectionDelegate,
)
from .collection_http_resource import (
    CreateCollectionRequest,
    UpdateCollectionRequest,
)
from .collection_record import (
    CollectionChangeRecord,
    CollectionContentMode,
    CollectionRecord,
    CollectionResourceRef,
)


class CollectionHttpDelegate(CollectionDelegate):
    __http_client: HttpClient

    def __init__(self, http_client: HttpClient):
        self.__http_client = http_client

    def create_collection(
        self,
        name: Optional[str] = None,
        description: Optional[str] = None,
        resources: Optional[list[CollectionResourceRef]] = None,
        tags: Optional[list[str]] = None,
        created_by: Optional[str] = None,
        org_id: Optional[str] = None,
    ) -> CollectionRecord:
        url = self.__http_client.url("v1/collections/create")
        headers = roboto_headers(
            user_id=created_by,
            org_id=org_id,
            resource_owner_id=org_id,
            additional_headers={"Content-Type": "application/json"},
        )

        data = pydantic_jsonable_dict(
            CreateCollectionRequest(
                name=name, description=description, resources=resources, tags=tags or []
            )
        )

        with RobotoHttpExceptionParse():
            return CollectionRecord.parse_obj(
                self.__http_client.post(url=url, headers=headers, data=data).from_json(
                    json_path=["data"]
                )
            )

    def get_collection(
        self,
        collection_id: str,
        org_id: Optional[str] = None,
        version: Optional[int] = None,
        content_mode: CollectionContentMode = CollectionContentMode.Full,
    ) -> CollectionRecord:
        url = self.__http_client.url(f"v1/collections/id/{collection_id}")

        query: dict[str, Any] = {"content_mode": content_mode.value}

        if version is not None:
            query["version"] = version

        url += "?" + urlencode(query)

        headers = roboto_headers(org_id=org_id, resource_owner_id=org_id)
        with RobotoHttpExceptionParse():
            return CollectionRecord.parse_obj(
                self.__http_client.get(url=url, headers=headers).from_json(
                    json_path=["data"]
                )
            )

    def get_collection_changes(
        self,
        collection_id: str,
        org_id: Optional[str] = None,
        from_version: Optional[int] = None,
        to_version: Optional[int] = None,
        page_token: Optional[str] = None,
    ) -> PaginatedList[CollectionChangeRecord]:
        url = self.__http_client.url(f"v1/collections/id/{collection_id}/changes")

        query: dict[str, Any] = {}

        if from_version:
            query["from_version"] = from_version

        if to_version:
            query["to_version"] = to_version

        if len(query.keys()) > 0:
            url += "?" + urlencode(query)

        headers = roboto_headers(org_id=org_id, resource_owner_id=org_id)

        with RobotoHttpExceptionParse():
            unmarshalled = self.__http_client.get(url=url, headers=headers).from_json(
                json_path=["data"]
            )

        return PaginatedList(
            items=[
                CollectionChangeRecord.parse_obj(item) for item in unmarshalled["items"]
            ],
            next_token=unmarshalled["next_token"],
        )

    def search_collections(
        self,
        query: QuerySpecification,
        org_id: Optional[str] = None,
        content_mode: CollectionContentMode = CollectionContentMode.SummaryOnly,
    ) -> PaginatedList[CollectionRecord]:
        url = self.__http_client.url(
            f"v1/collections/search?content_mode={content_mode.value}"
        )
        headers = roboto_headers(
            org_id=org_id,
            resource_owner_id=org_id,
            additional_headers={"Content-Type": "application/json"},
        )
        data = pydantic_jsonable_dict(query, exclude_none=True)

        with RobotoHttpExceptionParse():
            res = self.__http_client.post(url, data=data, headers=headers)

        unmarshalled = res.from_json(json_path=["data"])
        return PaginatedList(
            items=[
                CollectionRecord.parse_obj(dataset) for dataset in unmarshalled["items"]
            ],
            next_token=unmarshalled["next_token"],
        )

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
        url = self.__http_client.url(f"v1/collections/id/{collection_id}")
        headers = roboto_headers(
            user_id=updated_by,
            org_id=org_id,
            resource_owner_id=org_id,
            additional_headers={"Content-Type": "application/json"},
        )
        data = pydantic_jsonable_dict(
            UpdateCollectionRequest(
                name=name,
                description=description,
                add_resources=add_resources,
                remove_resources=remove_resources,
                add_tags=add_tags,
                remove_tags=remove_tags,
            )
        )

        with RobotoHttpExceptionParse():
            return CollectionRecord.parse_obj(
                self.__http_client.put(url=url, headers=headers, data=data).from_json(
                    json_path=["data"]
                )
            )

    def delete_collection(self, collection_id: str, org_id: Optional[str] = None):
        url = self.__http_client.url(f"v1/collections/id/{collection_id}")
        headers = roboto_headers(org_id=org_id, resource_owner_id=org_id)
        with RobotoHttpExceptionParse():
            self.__http_client.delete(url=url, headers=headers)
