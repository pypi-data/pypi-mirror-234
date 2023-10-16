#  Copyright (c) 2023 Roboto Technologies, Inc.


import datetime
from typing import Optional

import pydantic


class TokenContext(pydantic.BaseModel):
    token_id: str
    name: str
    description: Optional[str] = None
    expires: datetime.datetime
    last_used: Optional[datetime.datetime] = None


class TokenRecord(pydantic.BaseModel):
    secret: Optional[str] = None
    user_id: Optional[str] = None
    context: Optional[TokenContext] = None
