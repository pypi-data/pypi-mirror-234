#  Copyright (c) 2023 Roboto Technologies, Inc.

from typing import Any, Optional

from ...serde import pydantic_jsonable_dict
from .user_delegate import UserDelegate
from .user_record import UserRecord


class User:
    __record: UserRecord
    __user_delegate: UserDelegate

    @classmethod
    def from_id(cls, user_delegate: UserDelegate, user_id: Optional[str] = None):
        record = user_delegate.get_user_by_id(user_id=user_id)
        return cls(record=record, user_delegate=user_delegate)

    def __init__(self, record: UserRecord, user_delegate: UserDelegate):
        self.__record = record
        self.__user_delegate = user_delegate

    def to_dict(self, exclude_none: bool = False) -> dict[str, Any]:
        return pydantic_jsonable_dict(self.__record, exclude_none=exclude_none)

    def delete(self) -> None:
        return self.__user_delegate.delete_user(user_id=self.__record.user_id)

    def update(self, updates: dict[str, Any]) -> UserRecord:
        self.__record = self.__user_delegate.update_user(
            user_id=self.__record.user_id, updates=updates
        )
        return self.__record

    @property
    def user_id(self) -> str:
        return self.__record.user_id

    @property
    def username(self) -> str:
        return self.__record.user_id

    @property
    def is_system_user(self) -> bool:
        return (
            self.__record.is_system_user
            if self.__record.is_system_user is not None
            else False
        )

    @property
    def name(self) -> Optional[str]:
        return self.__record.name

    @property
    def picture_url(self) -> Optional[str]:
        return self.__record.picture_url

    @property
    def record(self) -> UserRecord:
        return self.__record
