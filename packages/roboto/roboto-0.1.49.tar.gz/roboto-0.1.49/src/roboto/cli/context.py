#  Copyright (c) 2023 Roboto Technologies, Inc.

from typing import Any, Optional

from ..domain.actions import (
    ActionDelegate,
    InvocationDelegate,
)
from ..domain.collections import (
    CollectionDelegate,
)
from ..domain.datasets import DatasetDelegate
from ..domain.files import FileDelegate
from ..domain.orgs import OrgDelegate
from ..domain.tokens import TokenDelegate
from ..domain.triggers import TriggerDelegate
from ..domain.users import UserDelegate
from ..http import HttpClient


class CLIContext:
    __roboto_service_base_url: Optional[str]
    __http: Optional[HttpClient]
    actions: ActionDelegate
    collections: CollectionDelegate
    datasets: DatasetDelegate
    files: FileDelegate
    invocations: InvocationDelegate
    orgs: OrgDelegate
    tokens: TokenDelegate
    triggers: TriggerDelegate
    users: UserDelegate
    extensions: dict[str, Any]

    @property
    def roboto_service_base_url(self) -> str:
        if self.__roboto_service_base_url is None:
            raise ValueError("roboto_service_base_url is unset")

        return self.__roboto_service_base_url

    @roboto_service_base_url.setter
    def roboto_service_base_url(self, roboto_service_base_url: str) -> None:
        self.__roboto_service_base_url = roboto_service_base_url

    @property
    def http(self) -> HttpClient:
        # Necessary since http is lazy set after parsing args
        if self.__http is None:
            raise ValueError("Unset HTTP client!")

        return self.__http

    @http.setter
    def http(self, http: HttpClient) -> None:
        self.__http = http
