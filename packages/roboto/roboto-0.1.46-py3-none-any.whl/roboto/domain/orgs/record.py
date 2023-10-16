#  Copyright (c) 2023 Roboto Technologies, Inc.

import enum

import pydantic

from ..users import UserRecord


class OrgStatus(str, enum.Enum):
    Provisioning = "provisioning"
    Active = "active"
    Deprovisioning = "de-provisioning"


class OrgTier(str, enum.Enum):
    free = "free"
    premium = "premium"


class OrgRecord(pydantic.BaseModel):
    org_id: str
    name: str
    tier: OrgTier
    members: int
    status: OrgStatus


class OrgRoleName(str, enum.Enum):
    user = "user"
    admin = "admin"
    owner = "owner"


class OrgRoleRecord(pydantic.BaseModel):
    user: UserRecord
    org: OrgRecord
    roles: list[OrgRoleName]


class OrgInviteRecord(pydantic.BaseModel):
    invite_id: str
    user_id: str
    invited_by: UserRecord
    org: OrgRecord
