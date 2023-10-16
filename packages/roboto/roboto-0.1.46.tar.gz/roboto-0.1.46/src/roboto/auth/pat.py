#  Copyright (c) 2023 Roboto Technologies, Inc.


import datetime
import pathlib
from typing import Any, Optional

import boto3
import jwt

from ..logging import default_logger
from ..profile import RobotoProfile

log = default_logger()

bearer_token_vendor = None
cred_finder = None

CREDENTIALS_FILE = pathlib.Path(f"{pathlib.Path.home()}/.roboto/credentials.json")
ROBOTO_TEMPDIR = pathlib.Path(f"{pathlib.Path.home()}/.roboto/tmp")
PROFILE_ENV_VAR = "ROBOTO_PROFILE"
USER_ENV_VAR = "ROBOTO_USER_ID"
TOKEN_ENV_VAR = "ROBOTO_ACCESS_TOKEN"


class RejectedTokenException(Exception):
    pass


class BearerTokenVendor:
    _client_id: str
    _cognito: Any
    _expires: datetime.datetime
    _id_token: Optional[str]
    _profile: RobotoProfile

    def __init__(
        self,
        client_id: str,
        cognito: Optional[Any] = None,
        profile: RobotoProfile = RobotoProfile(),
    ):
        self._client_id = client_id
        self._cognito = (
            cognito
            if cognito is not None
            else boto3.client("cognito-idp", region_name="us-west-2")
        )
        self._expires = datetime.datetime.now()
        self._id_token = None
        self._profile = profile

    def perform_cognito_handshake(self, user_id: str, token: str):
        try:
            res = self._cognito.initiate_auth(
                AuthFlow="CUSTOM_AUTH",
                ClientId=self._client_id,
                AuthParameters={"USERNAME": user_id},
            )

            if res["ChallengeName"] != "CUSTOM_CHALLENGE":
                raise RejectedTokenException(
                    f"Unexpected challenge {res['ChallengeName']}"
                )

            res = self._cognito.respond_to_auth_challenge(
                ClientId=self._client_id,
                ChallengeName="CUSTOM_CHALLENGE",
                Session=res["Session"],
                ChallengeResponses={"USERNAME": user_id, "ANSWER": token},
            )

            # Assume we have 60 fewer seconds to refresh than AWS is telling use we have
            expires_in = res["AuthenticationResult"]["ExpiresIn"] - 60
            expiry = datetime.datetime.now() + datetime.timedelta(seconds=expires_in)
            id_token = res["AuthenticationResult"]["IdToken"]

            return id_token, expiry
        except self._cognito.exceptions.NotAuthorizedException:
            raise RejectedTokenException("Authorization rejected by Cognito!")
        except self._cognito.exceptions.UserNotFoundException:
            raise RejectedTokenException(f"User {user_id} does not exist!")

    def refresh_tokens(self):
        now = datetime.datetime.now()
        entry = self._profile.get_entry()
        id_token_file = pathlib.Path(f"{ROBOTO_TEMPDIR}/{entry.token}_id_token")

        if id_token_file.exists():
            with open(id_token_file, "r") as f:
                content = f.read()

            # We don't need to verify signature because we'll get rejected by Roboto Service if the signature is invalid
            id_token = jwt.decode(content, options={"verify_signature": False})

            expires = datetime.datetime.fromtimestamp(id_token["exp"])
            if expires > now:
                self._expires = expires
                self._id_token = content
                return

        (
            self._id_token,
            self._expires,
        ) = self.perform_cognito_handshake(entry.user_id, entry.token)

        assert self._id_token is not None

        ROBOTO_TEMPDIR.mkdir(parents=True, exist_ok=True)
        with open(id_token_file, "w") as f:
            f.write(self._id_token)

    def get_id_token(self):
        now = datetime.datetime.now()
        if self._id_token is None or self._expires < now:
            log.debug("ID Token is unavailable or stale, regenerating it")
            self.refresh_tokens()
        else:
            log.debug("ID Token is already available!")

        return self._id_token

    def get_auth_header(self):
        return f"Bearer {self.get_id_token()}"
