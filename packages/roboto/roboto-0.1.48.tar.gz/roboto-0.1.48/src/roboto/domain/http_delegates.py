#  Copyright (c) 2023 Roboto Technologies, Inc.

import dataclasses

from ..http import HttpClient, PATAuthDecorator
from ..profile import RobotoProfile
from .actions import (
    ActionHttpDelegate,
    InvocationHttpDelegate,
)
from .collections import CollectionHttpDelegate
from .comments import CommentHttpDelegate
from .datasets import DatasetHttpDelegate
from .files import FileClientDelegate
from .orgs import OrgHttpDelegate
from .tokens import TokenHttpDelegate
from .triggers import TriggerHttpDelegate
from .users import UserHttpDelegate


@dataclasses.dataclass(frozen=True)
class HttpDelegates:
    http_client: HttpClient

    actions: ActionHttpDelegate
    collections: CollectionHttpDelegate
    datasets: DatasetHttpDelegate
    files: FileClientDelegate
    invocations: InvocationHttpDelegate
    orgs: OrgHttpDelegate
    tokens: TokenHttpDelegate
    triggers: TriggerHttpDelegate
    users: UserHttpDelegate
    comments: CommentHttpDelegate

    @staticmethod
    def from_client(http: HttpClient, endpoint: str) -> "HttpDelegates":
        # Take endpoint explicitly
        actions = ActionHttpDelegate(roboto_service_base_url=endpoint, http_client=http)
        datasets = DatasetHttpDelegate(
            roboto_service_base_url=endpoint, http_client=http
        )
        files = FileClientDelegate(roboto_service_base_url=endpoint, http_client=http)
        invocations = InvocationHttpDelegate(
            roboto_service_base_url=endpoint, http_client=http
        )

        # Take endpoint implicitly through client
        collections = CollectionHttpDelegate(http_client=http)
        comments = CommentHttpDelegate(http_client=http)
        orgs = OrgHttpDelegate(http_client=http)
        tokens = TokenHttpDelegate(http_client=http)
        triggers = TriggerHttpDelegate(http_client=http)
        users = UserHttpDelegate(http_client=http)

        return HttpDelegates(
            actions=actions,
            collections=collections,
            comments=comments,
            datasets=datasets,
            files=files,
            http_client=http,
            invocations=invocations,
            orgs=orgs,
            tokens=tokens,
            triggers=triggers,
            users=users,
        )

    @staticmethod
    def from_profile(profile: RobotoProfile, entry_name: str = "default"):
        entry = profile.get_entry(entry_name)
        auth = PATAuthDecorator.for_client(
            client_id=entry.default_client_id, profile=profile
        )
        http = HttpClient(default_endpoint=entry.default_endpoint, default_auth=auth)
        return HttpDelegates.from_client(http=http, endpoint=entry.default_endpoint)
