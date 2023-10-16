#  Copyright (c) 2023 Roboto Technologies, Inc.
import enum
import json
import os
import pathlib
from typing import Any, Optional

import pydantic

from ..logging import default_logger

log = default_logger()

PROFILE_ENV_VAR = "ROBOTO_PROFILE"

PROD_USER_POOL_CLIENT_ID = "1gricmdmh0vv582qdd84phab5"
PROD_ENDPOINT = "https://api.roboto.ai"

DEFAULT_ROBOTO_CONFIG_DIR = pathlib.Path.home() / ".roboto"
DEFAULT_ROBOTO_PROFILE_FILE = DEFAULT_ROBOTO_CONFIG_DIR / "config.json"


class RobotoProfileEntry(pydantic.BaseModel):
    user_id: str
    token: str
    default_endpoint: str = PROD_ENDPOINT
    default_client_id: str = PROD_USER_POOL_CLIENT_ID


class RobotoProfileFileType(str, enum.Enum):
    none = "none"
    malformed = "malformed"
    implicit = "implicit"
    explicit = "explicit"


class MissingProfileException(BaseException):
    pass


class MalformedProfileException(BaseException):
    pass


class RobotoProfile:
    __config_file: pathlib.Path
    __default_profile_name: str

    def __init__(
        self,
        config_file: pathlib.Path = DEFAULT_ROBOTO_PROFILE_FILE,
        default_profile_name: Optional[str] = None,
    ):
        self.__config_file = config_file
        self.__default_profile_name = (
            default_profile_name
            if default_profile_name is not None
            else os.environ.get(PROFILE_ENV_VAR, "default")
        )

    @property
    def config_dir(self) -> pathlib.Path:
        return self.__config_file.parent

    @property
    def config_file(self) -> pathlib.Path:
        return self.__config_file

    def get_entry(self, profile_name: Optional[str] = None) -> RobotoProfileEntry:
        profile_to_check = (
            profile_name if profile_name is not None else self.__default_profile_name
        )
        log.debug("Using profile '%s'", profile_to_check)
        # TODO - Support AWS style order of precedence
        file_type, entry = self.__base_entry_from_file(profile_to_check)

        if file_type is RobotoProfileFileType.malformed:
            raise MalformedProfileException(
                f"Malformed roboto profile file '{self.__config_file}'"
            )
        elif file_type is RobotoProfileFileType.none:
            raise MissingProfileException(
                f"Missing roboto profile file '{self.__config_file}'"
            )

        assert entry is not None
        return entry

    def __base_entry_from_file(
        self,
        profile_name: str,
    ) -> tuple[RobotoProfileFileType, Optional[RobotoProfileEntry]]:
        if not self.__config_file.is_file():
            return RobotoProfileFileType.none, None

        with open(self.__config_file, "r") as f:
            try:
                contents: dict[str, Any] = json.loads(f.read())
            except json.decoder.JSONDecodeError:
                return RobotoProfileFileType.malformed, None

        if profile_name in contents.keys():
            try:
                return RobotoProfileFileType.explicit, RobotoProfileEntry.parse_obj(
                    contents.get(profile_name)
                )
            except pydantic.ValidationError:
                log.warning(
                    f"Couldn't parse {self.__config_file} as a multi-profile 'explicit' type"
                )
                return RobotoProfileFileType.malformed, None

        try:
            return RobotoProfileFileType.implicit, RobotoProfileEntry.parse_obj(
                contents
            )
        except pydantic.ValidationError:
            log.warning(
                f"Couldn't parse {self.__config_file} as single-profile 'implicit' type"
            )
            return RobotoProfileFileType.malformed, None
