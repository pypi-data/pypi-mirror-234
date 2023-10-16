#  Copyright (c) 2023 Roboto Technologies, Inc.

RESOURCE_OWNER_OVERRIDE_HEADER = "X-Roboto-Resource-Owner-Id"
"""Header to specify the organization that owns the resource being accessed."""

RESOURCE_OWNER_OVERRIDE_QUERY_PARAM = "robotoResourceOwnerId"
"""Query parameter to specify the organization that owns the resource being accessed."""

ORG_OVERRIDE_HEADER = "X-Roboto-Org-Id"
"""Header to specify the organization that the user is acting on behalf of."""

ORG_OVERRIDE_QUERY_PARAM = "robotoOrgId"
"""Query parameter to specify the organization that the user is acting on behalf of."""

USER_OVERRIDE_HEADER = "X-Roboto-User-Id"
"""Header to specify the user that is performing the REST operation."""

USER_OVERRIDE_QUERY_PARAM = "robotoUserId"
""""Query parameter to specify the user that is performing the REST operation."""
