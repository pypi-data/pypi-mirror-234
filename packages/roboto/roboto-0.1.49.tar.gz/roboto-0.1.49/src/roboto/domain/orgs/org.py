#  Copyright (c) 2023 Roboto Technologies, Inc.

from typing import Any, Optional

from ...serde import pydantic_jsonable_dict
from .delegate import OrgDelegate
from .record import (
    OrgRecord,
    OrgRoleName,
    OrgStatus,
)


class Org:
    __record: OrgRecord
    __org_delegate: OrgDelegate

    @classmethod
    def create(
        cls,
        name: str,
        org_delegate: OrgDelegate,
        bind_email_domain: bool = False,
        creator_user_id: Optional[str] = None,
    ):
        record = org_delegate.create_org(
            creator_user_id=creator_user_id,
            name=name,
            bind_email_domain=bind_email_domain,
        )
        return cls(record=record, org_delegate=org_delegate)

    @classmethod
    def from_id(cls, org_id: str, org_delegate: OrgDelegate) -> "Org":
        record = org_delegate.get_org_by_id(org_id=org_id)
        return cls(record=record, org_delegate=org_delegate)

    @classmethod
    def for_user(
        cls, org_delegate: OrgDelegate, user_id: Optional[str] = None
    ) -> list["Org"]:
        records = org_delegate.orgs_for_user(user_id=user_id)
        return [cls(record=record, org_delegate=org_delegate) for record in records]

    @property
    def record(self) -> OrgRecord:
        return self.__record

    def update(
        self, updates: dict[str, Any], caller_user_id: Optional[str] = None
    ) -> "Org":
        self.__record = self.__org_delegate.update_org(
            updates=updates, org_id=self.org_id, caller_user_id=caller_user_id
        )
        return self

    def delete(self) -> None:
        self.__org_delegate.delete_org(org_id=self.org_id)

    def bind_email_domain(self, email_domain: str) -> None:
        self.__org_delegate.bind_email_domain(
            org_id=self.__record.org_id, email_domain=email_domain
        )

    def unbind_email_domain(self, email_domain: str) -> None:
        self.__org_delegate.unbind_email_domain(
            org_id=self.__record.org_id, email_domain=email_domain
        )

    def list_email_domains(self) -> list[str]:
        return self.__org_delegate.get_email_domains_for_org(
            org_id=self.__record.org_id
        )

    def remove_user(self, user_id: str) -> None:
        """
        Remove a user from an organization.

        Args:
            user_id: The user_id of the user to remove from this organization.

        Raises:
            roboto.exceptions.RobotoUnauthorizedException: In a number of different cases:
                - The caller is not a member of this org
                - The caller is not an org administrator or owner of this org
                - The caller is an administrator but not an owner, and the target user is also an administrator
            roboto.exceptions.RobotoNotFoundException: If the target user is not a member of the specified org.
            roboto.exceptions.RobotoInvalidRequestException:
                If the caller is trying to remove themselves from the org, and the caller is the owner of that org.
                The admin should transfer ownership of the org to another user before removing themselves.

        Returns:
            None
        """
        self.__org_delegate.remove_user_from_org(user_id=user_id, org_id=self.org_id)

    def add_role_for_user(self, user_id: str, role_name: OrgRoleName):
        self.__org_delegate.add_role_for_user(
            user_id=user_id, role_name=role_name, org_id=self.org_id
        )

    def remove_role_from_user(self, user_id: str, role_name: OrgRoleName):
        self.__org_delegate.remove_role_from_user(
            user_id=user_id, role_name=role_name, org_id=self.org_id
        )

    def __init__(self, record: OrgRecord, org_delegate: OrgDelegate):
        self.__record = record
        self.__org_delegate = org_delegate

    def to_dict(self) -> dict[str, Any]:
        return pydantic_jsonable_dict(self.__record)

    @property
    def org_id(self):
        return self.__record.org_id

    @property
    def status(self) -> OrgStatus:
        return self.__record.status
