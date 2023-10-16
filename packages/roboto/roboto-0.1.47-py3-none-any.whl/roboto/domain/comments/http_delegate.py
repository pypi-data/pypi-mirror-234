from typing import Optional

from ...exceptions import RobotoHttpExceptionParse
from ...http import (
    HttpClient,
    PaginatedList,
    roboto_headers,
)
from ...serde import pydantic_jsonable_dict
from .delegate import CommentDelegate
from .http_resources import (
    CreateCommentRequest,
    UpdateCommentRequest,
)
from .record import CommentRecord, EntityType


class CommentHttpDelegate(CommentDelegate):
    __http_client: HttpClient

    def __init__(self, http_client: HttpClient):
        super().__init__()
        self.__http_client = http_client

    def create_comment(
        self,
        entity_type: EntityType,
        entity_id: str,
        comment_text: str,
        org_id: Optional[str] = None,
        created_by: Optional[str] = None,
    ) -> CommentRecord:
        url = self.__http_client.url("v1/comments")

        headers = roboto_headers(
            org_id=org_id,
            user_id=created_by,
            additional_headers={"Content-Type": "application/json"},
        )

        request_body = CreateCommentRequest(
            entity_type=entity_type,
            entity_id=entity_id,
            comment_text=comment_text,
        )

        with RobotoHttpExceptionParse():
            response = self.__http_client.post(
                url=url, headers=headers, data=pydantic_jsonable_dict(request_body)
            )

        return CommentRecord.parse_obj(response.from_json(json_path=["data"]))

    def get_comment_by_id(
        self,
        comment_id: str,
        org_id: Optional[str] = None,
    ) -> CommentRecord:
        url = self.__http_client.url(f"v1/comments/{comment_id}")

        with RobotoHttpExceptionParse():
            response = self.__http_client.get(url=url)

        return CommentRecord.parse_obj(response.from_json(json_path=["data"]))

    def delete_comment(
        self,
        record: CommentRecord,
    ) -> None:
        url = self.__http_client.url(f"v1/comments/{record.comment_id}")

        with RobotoHttpExceptionParse():
            self.__http_client.delete(url=url)

    def update_comment(
        self,
        record: CommentRecord,
        comment_text: str,
    ) -> CommentRecord:
        url = self.__http_client.url(f"v1/comments/{record.comment_id}")

        req = UpdateCommentRequest(
            comment_text=comment_text,
        )

        body = pydantic_jsonable_dict(req, exclude_unset=True)

        with RobotoHttpExceptionParse():
            response = self.__http_client.put(
                url=url,
                data=body,
            )

        return CommentRecord.parse_obj(response.from_json(json_path=["data"]))

    def get_comments_by_entity(
        self,
        entity_type: EntityType,
        entity_id: str,
        org_id: Optional[str] = None,
        page_token: Optional[str] = None,
    ) -> PaginatedList[CommentRecord]:
        url = self.__http_client.url(f"v1/comments/{entity_type}/{entity_id}")

        if page_token:
            url = f"{url}?page_token={page_token}"

        with RobotoHttpExceptionParse():
            response = self.__http_client.get(url=url)

        parsed_items = []

        unmarshalled = response.from_json(json_path=["data"])

        data_items = unmarshalled["items"]
        next_token = unmarshalled["next_token"]

        for item in data_items:
            parsed_items.append(CommentRecord.parse_obj(item))

        return PaginatedList(items=parsed_items, next_token=next_token)

    def get_comments_by_entity_type(
        self,
        entity_type: EntityType,
        org_id: Optional[str] = None,
        page_token: Optional[str] = None,
    ) -> PaginatedList[CommentRecord]:
        url = self.__http_client.url(f"v1/comments/type/{entity_type}")

        if page_token:
            url = f"{url}?page_token={page_token}"

        with RobotoHttpExceptionParse():
            response = self.__http_client.get(url=url)

        parsed_items = []

        unmarshalled = response.from_json(json_path=["data"])

        data_items = unmarshalled["items"]
        next_token = unmarshalled["next_token"]

        for item in data_items:
            parsed_items.append(CommentRecord.parse_obj(item))

        return PaginatedList(items=parsed_items, next_token=next_token)

    def get_comments_by_user(
        self,
        user_id: str,
        org_id: Optional[str] = None,
        page_token: Optional[str] = None,
    ) -> PaginatedList[CommentRecord]:
        url = self.__http_client.url(f"v1/comments/user/{user_id}")

        if page_token:
            url = f"{url}?page_token={page_token}"

        with RobotoHttpExceptionParse():
            response = self.__http_client.get(url=url)

        parsed_items = []

        unmarshalled = response.from_json(json_path=["data"])

        data_items = unmarshalled["items"]
        next_token = unmarshalled["next_token"]

        for item in data_items:
            parsed_items.append(CommentRecord.parse_obj(item))

        return PaginatedList(items=parsed_items, next_token=next_token)
