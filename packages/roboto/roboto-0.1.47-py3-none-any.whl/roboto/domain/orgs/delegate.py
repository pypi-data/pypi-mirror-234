#  Copyright (c) 2023 Roboto Technologies, Inc.

import abc
from typing import Any, Optional

from .record import (
    OrgInviteRecord,
    OrgRecord,
    OrgRoleName,
    OrgRoleRecord,
)


class OrgDelegate(abc.ABC):
    @abc.abstractmethod
    def create_org(
        self,
        creator_user_id: Optional[str],
        name: str,
        bind_email_domain: bool = False,
    ) -> OrgRecord:
        raise NotImplementedError("create_org")

    @abc.abstractmethod
    def update_org(
        self,
        updates: dict[str, Any],
        org_id: Optional[str] = None,
        caller_user_id: Optional[str] = None,
    ) -> OrgRecord:
        raise NotImplementedError("update_org")

    @abc.abstractmethod
    def orgs_for_user(self, user_id: Optional[str]) -> list[OrgRecord]:
        raise NotImplementedError("orgs_for_user")

    @abc.abstractmethod
    def org_roles_for_user(self, user_id: Optional[str]) -> list[OrgRoleRecord]:
        raise NotImplementedError("org_roles_for_user")

    @abc.abstractmethod
    def org_roles_for_org(self, org_id: Optional[str]) -> list[OrgRoleRecord]:
        raise NotImplementedError("org_roles_for_org")

    @abc.abstractmethod
    def org_role_for_user_in_org(
        self, user_id: Optional[str] = None, org_id: Optional[str] = None
    ) -> OrgRoleRecord:
        raise NotImplementedError("org_role_for_user_in_org")

    @abc.abstractmethod
    def add_role_for_user(
        self, user_id: str, role_name: OrgRoleName, org_id: Optional[str] = None
    ):
        raise NotImplementedError("add_role_for_user")

    @abc.abstractmethod
    def remove_role_from_user(
        self, user_id: str, role_name: OrgRoleName, org_id: Optional[str] = None
    ):
        raise NotImplementedError("remove_role_for_user")

    @abc.abstractmethod
    def remove_user_from_org(self, user_id: str, org_id: Optional[str] = None) -> None:
        raise NotImplementedError("remove_user_from_org")

    @abc.abstractmethod
    def get_org_by_id(self, org_id: str) -> OrgRecord:
        raise NotImplementedError("get_org_by_id")

    @abc.abstractmethod
    def delete_org(self, org_id: str):
        raise NotImplementedError("delete_org")

    @abc.abstractmethod
    def bind_email_domain(self, org_id: str, email_domain: str):
        raise NotImplementedError("bind_email_domain")

    @abc.abstractmethod
    def unbind_email_domain(self, email_domain: str, org_id: Optional[str] = None):
        raise NotImplementedError("unbind_email_domain")

    @abc.abstractmethod
    def get_email_domains_for_org(self, org_id: Optional[str] = None) -> list[str]:
        raise NotImplementedError("get_email_domains_for_org")

    @abc.abstractmethod
    def invite_user_to_org(
        self, invited_user_id: str, org_id: str, inviting_user_id: Optional[str] = None
    ) -> OrgInviteRecord:
        raise NotImplementedError("invite_user_to_org")

    @abc.abstractmethod
    def get_invites_for_org(
        self, org_id: Optional[str] = None
    ) -> list[OrgInviteRecord]:
        raise NotImplementedError("get_invites_for_org")

    @abc.abstractmethod
    def accept_org_invite(self, invite_id: str, user_id: Optional[str] = None):
        raise NotImplementedError("accept_org_invite")

    @abc.abstractmethod
    def decline_org_invite(self, invite_id: str, user_id: Optional[str] = None):
        raise NotImplementedError("accept_org_invite")

    @abc.abstractmethod
    def get_org_invite(
        self, invite_id: str, user_id: Optional[str] = None
    ) -> OrgInviteRecord:
        raise NotImplementedError("get_org_invite")
