#  Copyright (c) 2023 Roboto Technologies, Inc.
import abc
from typing import Optional

from .record import TokenRecord


class TokenDelegate(abc.ABC):
    @abc.abstractmethod
    def get_tokens_for_user(self, user_id: Optional[str] = None) -> list[TokenRecord]:
        raise NotImplementedError("get_tokens_for_user")

    @abc.abstractmethod
    def create_token(
        self,
        expiry_days: int,
        name: str,
        user_id: Optional[str] = None,
        description: Optional[str] = None,
    ) -> TokenRecord:
        raise NotImplementedError("create_token")

    @abc.abstractmethod
    def delete_token(self, token_id: str) -> None:
        raise NotImplementedError("delete_token")

    @abc.abstractmethod
    def get_token_by_token_id(self, token_id: str) -> TokenRecord:
        raise NotImplementedError("get_token_by_token_id")
