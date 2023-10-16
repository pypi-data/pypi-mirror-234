#  Copyright (c) 2023 Roboto Technologies, Inc.


from typing import Optional

import pydantic


class CreateTokenRequest(pydantic.BaseModel):
    expiry_days: int
    name: str
    description: Optional[str] = None


class ValidateTokenResponse(pydantic.BaseModel):
    valid: bool
