from typing import Optional

from ...http import PaginatedList
from .delegate import CommentDelegate
from .record import CommentRecord, EntityType


class Comment:
    __comment_delegate: CommentDelegate
    __record: CommentRecord

    @classmethod
    def create(
        cls,
        comment_text: str,
        entity_id: str,
        entity_type: EntityType,
        comment_delegate: CommentDelegate,
        created_by: Optional[str] = None,
        org_id: Optional[str] = None,
    ) -> "Comment":
        record = comment_delegate.create_comment(
            entity_type,
            entity_id,
            comment_text,
            org_id,
            created_by,
        )
        return cls(record, comment_delegate)

    @classmethod
    def from_id(
        cls,
        comment_id: str,
        comment_delegate: CommentDelegate,
        org_id: Optional[str] = None,
    ) -> "Comment":
        record = comment_delegate.get_comment_by_id(comment_id, org_id)
        return cls(record, comment_delegate)

    @classmethod
    def for_entity(
        cls,
        comment_delegate: CommentDelegate,
        entity_type: EntityType,
        entity_id: str,
        org_id: Optional[str] = None,
        page_token: Optional[str] = None,
    ) -> PaginatedList[CommentRecord]:
        return comment_delegate.get_comments_by_entity(
            entity_type, entity_id, org_id, page_token
        )

    @classmethod
    def for_entity_type(
        cls,
        comment_delegate: CommentDelegate,
        entity_type: EntityType,
        org_id: Optional[str] = None,
        page_token: Optional[str] = None,
    ) -> PaginatedList[CommentRecord]:
        return comment_delegate.get_comments_by_entity_type(
            entity_type, org_id, page_token
        )

    @classmethod
    def for_user(
        cls,
        comment_delegate: CommentDelegate,
        user_id: str,
        org_id: Optional[str] = None,
        page_token: Optional[str] = None,
    ) -> PaginatedList[CommentRecord]:
        return comment_delegate.get_comments_by_user(user_id, org_id, page_token)

    def __init__(
        self,
        record: CommentRecord,
        comment_delegate: CommentDelegate,
    ) -> None:
        self.__comment_delegate = comment_delegate
        self.__record = record

    @property
    def record(self) -> CommentRecord:
        return self.__record

    def delete_comment(self) -> None:
        self.__comment_delegate.delete_comment(self.__record)

    def update_comment(self, comment_text: str) -> None:
        self.__record = self.__comment_delegate.update_comment(
            self.__record, comment_text
        )
