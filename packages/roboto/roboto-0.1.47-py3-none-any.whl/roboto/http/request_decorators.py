#  Copyright (c) 2023 Roboto Technologies, Inc.
import os
from typing import Optional

import boto3
from botocore.auth import SigV4Auth
from botocore.awsrequest import AWSRequest
from botocore.credentials import (
    ReadOnlyCredentials,
)

from ..auth.pat import BearerTokenVendor
from ..logging import default_logger
from ..profile import RobotoProfile
from .constants import USER_OVERRIDE_HEADER
from .http_client import HttpRequest

logger = default_logger()


class LocalAuthDecorator:
    __user_id: str

    def __init__(self, user_id: str):
        self.__user_id = user_id

    def __call__(self, request: HttpRequest) -> HttpRequest:
        if request.headers is None:
            request.headers = {}

        request.headers[USER_OVERRIDE_HEADER] = self.__user_id
        return request


class PATAuthDecorator:
    _token_vendor: BearerTokenVendor

    def __init__(self, token_vendor: BearerTokenVendor):
        self._token_vendor = token_vendor

    def __call__(self, request: HttpRequest) -> HttpRequest:
        if request.headers is None:
            request.headers = {}

        request.headers["Authorization"] = self._token_vendor.get_auth_header()
        return request

    @staticmethod
    def for_client(client_id: str, profile: RobotoProfile = RobotoProfile(), **kwargs):
        token_vendor = BearerTokenVendor(client_id=client_id, profile=profile, **kwargs)
        return PATAuthDecorator(token_vendor=token_vendor)


class SigV4AuthDecorator:
    __credentials: ReadOnlyCredentials
    __region: str
    __service: str

    @staticmethod
    def lookup_credentials() -> ReadOnlyCredentials:
        session = boto3.Session()
        creds = session.get_credentials()
        if creds is None:
            raise RuntimeError("No AWS credentials found")

        return creds.get_frozen_credentials()

    @staticmethod
    def lookup_region() -> str:
        session = boto3.Session()
        if session.region_name:
            return session.region_name

        region = os.environ.get("AWS_REGION", os.environ.get("AWS_DEFAULT_REGION"))
        if not region:
            raise ValueError("One of AWS_REGION or AWS_DEFAULT_REGION must be set.")
        return region

    def __init__(
        self,
        service: str = "execute-api",
        credentials: Optional[ReadOnlyCredentials] = None,
        region: Optional[str] = None,
    ):
        self.__credentials = (
            credentials if credentials else SigV4AuthDecorator.lookup_credentials()
        )
        self.__region = region if region else SigV4AuthDecorator.lookup_region()
        self.__service = service

    def __call__(self, request: HttpRequest) -> HttpRequest:
        if "Host" not in request.headers:
            request.append_headers({"Host": request.hostname})

        aws_request = AWSRequest(
            method=request.method.upper(), url=request.url, data=request.body
        )
        aws_request.context["payload_signing_enabled"] = True
        SigV4Auth(self.__credentials, self.__service, self.__region).add_auth(
            aws_request
        )
        request.append_headers(dict(aws_request.headers.items()))
        return request
