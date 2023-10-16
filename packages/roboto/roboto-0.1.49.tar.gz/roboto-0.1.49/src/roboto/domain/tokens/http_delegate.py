#  Copyright (c) 2023 Roboto Technologies, Inc.

from typing import Optional

from ...exceptions import RobotoHttpExceptionParse
from ...http import HttpClient, roboto_headers
from ...serde import pydantic_jsonable_dict
from .delegate import TokenDelegate
from .http_resources import CreateTokenRequest
from .record import TokenRecord


class TokenHttpDelegate(TokenDelegate):
    __http_client: HttpClient

    def __init__(self, http_client: HttpClient):
        super().__init__()
        self.__http_client = http_client

    def get_tokens_for_user(self, user_id: Optional[str] = None) -> list[TokenRecord]:
        url = self.__http_client.url("v1/tokens")
        headers = roboto_headers(user_id=user_id)

        with RobotoHttpExceptionParse():
            response = self.__http_client.get(url=url, headers=headers)

        unmarshalled = response.from_json(json_path=["data"])
        return [TokenRecord.parse_obj(record) for record in unmarshalled]

    def create_token(
        self,
        expiry_days: int,
        name: str,
        user_id: Optional[str] = None,
        description: Optional[str] = None,
    ) -> TokenRecord:
        url = self.__http_client.url("v1/tokens")
        headers = roboto_headers(
            user_id=user_id, additional_headers={"Content-Type": "application/json"}
        )

        data = CreateTokenRequest(
            expiry_days=expiry_days, name=name, description=description
        )

        with RobotoHttpExceptionParse():
            response = self.__http_client.post(
                url=url, headers=headers, data=pydantic_jsonable_dict(data)
            )
        return TokenRecord.parse_obj(response.from_json(json_path=["data"]))

    def delete_token(self, token_id: str) -> None:
        url = self.__http_client.url(f"v1/tokens/{token_id}")

        with RobotoHttpExceptionParse():
            self.__http_client.delete(url=url)

    def get_token_by_token_id(self, token_id: str) -> TokenRecord:
        url = self.__http_client.url(f"v1/tokens/{token_id}")

        with RobotoHttpExceptionParse():
            response = self.__http_client.get(url=url)
        return TokenRecord.parse_obj(response.from_json(json_path=["data"]))
