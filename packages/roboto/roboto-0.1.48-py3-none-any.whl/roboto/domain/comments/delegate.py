import abc
from typing import Optional

from ...http import PaginatedList
from .record import CommentRecord, EntityType


class CommentDelegate(abc.ABC):
    @abc.abstractmethod
    def create_comment(
        self,
        entity_type: EntityType,
        entity_id: str,
        comment_text: str,
        org_id: Optional[str] = None,
        created_by: Optional[str] = None,
    ) -> CommentRecord:
        raise NotImplementedError("create_comment")

    @abc.abstractmethod
    def get_comment_by_id(
        self,
        comment_id: str,
        org_id: Optional[str] = None,
    ) -> CommentRecord:
        raise NotImplementedError("get_comment_by_id")

    @abc.abstractmethod
    def delete_comment(
        self,
        record: CommentRecord,
    ) -> None:
        raise NotImplementedError("delete_comment")

    @abc.abstractmethod
    def update_comment(
        self,
        record: CommentRecord,
        comment_text: str,
    ) -> CommentRecord:
        raise NotImplementedError("update_comment")

    @abc.abstractmethod
    def get_comments_by_entity(
        self,
        entity_type: EntityType,
        entity_id: str,
        org_id: Optional[str] = None,
        page_token: Optional[str] = None,
    ) -> PaginatedList[CommentRecord]:
        raise NotImplementedError("get_comments_by_entity")

    @abc.abstractmethod
    def get_comments_by_entity_type(
        self,
        entity_type: EntityType,
        org_id: Optional[str] = None,
        page_token: Optional[str] = None,
    ) -> PaginatedList[CommentRecord]:
        raise NotImplementedError("get_comments_by_entity_type")

    @abc.abstractmethod
    def get_comments_by_user(
        self,
        user_id: str,
        org_id: Optional[str] = None,
        page_token: Optional[str] = None,
    ) -> PaginatedList[CommentRecord]:
        raise NotImplementedError("get_comments_by_user")
