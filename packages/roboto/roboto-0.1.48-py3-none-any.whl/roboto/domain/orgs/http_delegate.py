#  Copyright (c) 2023 Roboto Technologies, Inc.

from typing import Any, Optional

from ...exceptions import RobotoHttpExceptionParse
from ...http import HttpClient, roboto_headers
from ...serde import pydantic_jsonable_dict
from .delegate import OrgDelegate
from .http_resources import (
    BindEmailDomainRequest,
    CreateOrgRequest,
    InviteUserRequest,
    ModifyRoleForUserRequest,
    OrgRecordUpdates,
    RemoveUserFromOrgRequest,
    UpdateOrgRequest,
)
from .record import (
    OrgInviteRecord,
    OrgRecord,
    OrgRoleName,
    OrgRoleRecord,
)


class OrgHttpDelegate(OrgDelegate):
    __http_client: HttpClient

    def __init__(self, http_client: HttpClient):
        super().__init__()
        self.__http_client = http_client

    def create_org(
        self,
        creator_user_id: Optional[str],
        name: str,
        bind_email_domain: bool = False,
    ) -> OrgRecord:
        url = self.__http_client.url("v1/orgs")
        headers = roboto_headers(user_id=creator_user_id)
        headers["Content-Type"] = "application/json"

        request_body = CreateOrgRequest(name=name, bind_email_domain=bind_email_domain)

        with RobotoHttpExceptionParse():
            response = self.__http_client.post(
                url=url, headers=headers, data=pydantic_jsonable_dict(request_body)
            )

        return OrgRecord.parse_obj(response.from_json(json_path=["data"]))

    def update_org(
        self,
        updates: dict[str, Any],
        org_id: Optional[str] = None,
        caller_user_id: Optional[str] = None,
    ) -> OrgRecord:
        url = self.__http_client.url("v1/orgs")
        headers = roboto_headers(user_id=caller_user_id, org_id=org_id)
        headers["Content-Type"] = "application/json"
        request_body = UpdateOrgRequest(updates=OrgRecordUpdates.parse_obj(updates))

        with RobotoHttpExceptionParse():
            response = self.__http_client.put(
                url=url,
                headers=headers,
                data=pydantic_jsonable_dict(request_body, exclude_unset=True),
            )

        return OrgRecord.parse_obj(response.from_json(json_path=["data"]))

    def orgs_for_user(self, user_id: Optional[str]) -> list[OrgRecord]:
        url = self.__http_client.url("v1/users/orgs")

        with RobotoHttpExceptionParse():
            response = self.__http_client.get(url=url)

        return [
            OrgRecord.parse_obj(record)
            for record in response.from_json(json_path=["data"])
        ]

    def org_roles_for_user(self, user_id: Optional[str]) -> list[OrgRoleRecord]:
        url = self.__http_client.url("v1/users/roles")

        headers = roboto_headers(user_id=user_id)

        with RobotoHttpExceptionParse():
            response = self.__http_client.get(url=url, headers=headers)

        return [
            OrgRoleRecord.parse_obj(record)
            for record in response.from_json(json_path=["data"])
        ]

    def add_role_for_user(
        self, user_id: str, role_name: OrgRoleName, org_id: Optional[str] = None
    ):
        url = self.__http_client.url("v1/orgs/roles")
        headers = roboto_headers(org_id=org_id)
        request_body = ModifyRoleForUserRequest(user_id=user_id, role_name=role_name)

        with RobotoHttpExceptionParse():
            self.__http_client.put(
                url=url, headers=headers, data=pydantic_jsonable_dict(request_body)
            )

    def remove_role_from_user(
        self, user_id: str, role_name: OrgRoleName, org_id: Optional[str] = None
    ):
        url = self.__http_client.url("v1/orgs/roles")
        headers = roboto_headers(org_id=org_id)
        request_body = ModifyRoleForUserRequest(user_id=user_id, role_name=role_name)

        with RobotoHttpExceptionParse():
            self.__http_client.delete(
                url=url, headers=headers, data=pydantic_jsonable_dict(request_body)
            )

    def org_roles_for_org(self, org_id: Optional[str]) -> list[OrgRoleRecord]:
        url = self.__http_client.url("v1/orgs/roles")

        headers = roboto_headers(org_id=org_id)

        with RobotoHttpExceptionParse():
            response = self.__http_client.get(url=url, headers=headers)

        return [
            OrgRoleRecord.parse_obj(record)
            for record in response.from_json(json_path=["data"])
        ]

    def remove_user_from_org(self, user_id: str, org_id: Optional[str] = None) -> None:
        url = self.__http_client.url("v1/orgs/users")

        headers = roboto_headers(org_id=org_id)

        request_body = RemoveUserFromOrgRequest(user_id=user_id)

        with RobotoHttpExceptionParse():
            self.__http_client.delete(
                url=url, headers=headers, data=pydantic_jsonable_dict(request_body)
            )

    def get_org_by_id(self, org_id: str) -> OrgRecord:
        url = self.__http_client.url("v1/orgs")
        headers = roboto_headers(org_id=org_id)

        with RobotoHttpExceptionParse():
            response = self.__http_client.get(url=url, headers=headers)

        return OrgRecord.parse_obj(response.from_json(json_path=["data"]))

    def delete_org(self, org_id: str) -> None:
        url = self.__http_client.url("v1/orgs")
        headers = roboto_headers(org_id=org_id)

        with RobotoHttpExceptionParse():
            self.__http_client.delete(url=url, headers=headers)

    def bind_email_domain(self, org_id: str, email_domain: str):
        url = self.__http_client.url("v1/orgs/subdomains")
        headers = roboto_headers(org_id=org_id)
        request_body = BindEmailDomainRequest(email_domain=email_domain)

        with RobotoHttpExceptionParse():
            self.__http_client.put(
                url=url, headers=headers, data=pydantic_jsonable_dict(request_body)
            )

    def unbind_email_domain(self, email_domain: str, org_id: Optional[str] = None):
        url = self.__http_client.url("v1/orgs/subdomains")
        headers = roboto_headers(org_id=org_id)
        request_body = BindEmailDomainRequest(email_domain=email_domain)

        with RobotoHttpExceptionParse():
            self.__http_client.delete(
                url=url, headers=headers, data=pydantic_jsonable_dict(request_body)
            )

    def get_email_domains_for_org(self, org_id: Optional[str] = None) -> list[str]:
        url = self.__http_client.url("v1/orgs/subdomains")
        headers = roboto_headers(org_id=org_id)

        with RobotoHttpExceptionParse():
            response = self.__http_client.get(url=url, headers=headers)
            return response.from_json()["data"]

    def invite_user_to_org(
        self, invited_user_id: str, org_id: str, inviting_user_id: Optional[str] = None
    ) -> OrgInviteRecord:
        url = self.__http_client.url("v1/orgs/invites")
        headers = roboto_headers(org_id=org_id)
        request_body = InviteUserRequest(invited_user_id=invited_user_id)

        with RobotoHttpExceptionParse():
            response = self.__http_client.post(
                url=url, headers=headers, data=pydantic_jsonable_dict(request_body)
            )

        return OrgInviteRecord.parse_obj(response.from_json(json_path=["data"]))

    def accept_org_invite(self, invite_id: str, user_id: Optional[str] = None):
        url = self.__http_client.url(f"v1/orgs/invites/{invite_id}/accept")

        with RobotoHttpExceptionParse():
            self.__http_client.post(url=url)

    def decline_org_invite(self, invite_id: str, user_id: Optional[str] = None):
        url = self.__http_client.url(f"v1/orgs/invites/{invite_id}/decline")

        with RobotoHttpExceptionParse():
            self.__http_client.post(url=url)

    def get_org_invite(
        self, invite_id: str, user_id: Optional[str] = None
    ) -> OrgInviteRecord:
        url = self.__http_client.url(f"v1/orgs/invites/{invite_id}")

        with RobotoHttpExceptionParse():
            response = self.__http_client.get(url=url)
        return OrgInviteRecord.parse_obj(response.from_json(json_path=["data"]))

    def get_invites_for_org(
        self, org_id: Optional[str] = None
    ) -> list[OrgInviteRecord]:
        url = self.__http_client.url("v1/orgs/invites")
        headers = roboto_headers(org_id=org_id)

        with RobotoHttpExceptionParse():
            response = self.__http_client.get(url=url, headers=headers)

        return [
            OrgInviteRecord.parse_obj(record)
            for record in response.from_json(json_path=["data"])
        ]

    def org_role_for_user_in_org(
        self, user_id: Optional[str] = None, org_id: Optional[str] = None
    ) -> OrgRoleRecord:
        assert user_id is not None

        url = self.__http_client.url(f"v1/orgs/roles/{user_id}")

        with RobotoHttpExceptionParse():
            response = self.__http_client.get(url=url)
        return OrgRoleRecord.parse_obj(response.from_json(json_path=["data"]))
