#  Copyright (c) 2023 Roboto Technologies, Inc.

from typing import Any, Optional

from ...serde import pydantic_jsonable_dict
from .delegate import TokenDelegate
from .record import TokenRecord


class Token:
    __record: TokenRecord
    __token_delegate: TokenDelegate

    @classmethod
    def from_id(cls, token_id: str, token_delegate: TokenDelegate) -> "Token":
        record = token_delegate.get_token_by_token_id(token_id=token_id)
        return cls(record=record, token_delegate=token_delegate)

    @classmethod
    def for_user(
        cls, token_delegate: TokenDelegate, user_id: Optional[str] = None
    ) -> list["Token"]:
        records = token_delegate.get_tokens_for_user(user_id=user_id)
        return [cls(record=record, token_delegate=token_delegate) for record in records]

    @classmethod
    def create(
        cls,
        expiry_days: int,
        name: str,
        token_delegate: TokenDelegate,
        user_id: Optional[str] = None,
        description: Optional[str] = None,
    ):
        record = token_delegate.create_token(
            user_id=user_id, expiry_days=expiry_days, name=name, description=description
        )
        return cls(record=record, token_delegate=token_delegate)

    def __init__(self, record: TokenRecord, token_delegate: TokenDelegate):
        self.__record = record
        self.__token_delegate = token_delegate

    @property
    def record(self) -> TokenRecord:
        return self.__record

    @property
    def secret(self) -> Optional[str]:
        return self.__record.secret

    @property
    def user_id(self) -> Optional[str]:
        return self.__record.user_id

    @property
    def token_id(self) -> Optional[str]:
        return None if self.__record.context is None else self.__record.context.token_id

    def delete(self):
        assert self.__record.context is not None
        return self.__token_delegate.delete_token(
            token_id=self.__record.context.token_id
        )

    def to_dict(self, exclude_none: bool = False) -> dict[str, Any]:
        return pydantic_jsonable_dict(self.__record, exclude_none=exclude_none)
