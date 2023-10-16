#  Copyright (c) 2023 Roboto Technologies, Inc.

import datetime
from distutils.version import StrictVersion
import importlib.metadata
import os
import sys
from typing import Optional

import pydantic

from roboto.http import HttpClient
from roboto.profile import RobotoProfile
from roboto.time import utcnow

from .terminal import AnsiColor


class CLIState(pydantic.BaseModel):
    last_checked_version: Optional[datetime.datetime]
    last_version: str = "0.0.0"
    out_of_date: bool = True


def check_last_update(profile: RobotoProfile):
    roboto_tmp_dir = profile.config_dir / "tmp"
    roboto_tmp_dir.mkdir(parents=True, exist_ok=True)
    cli_state_file = roboto_tmp_dir / "cli_state.json"

    last_version = None
    version = importlib.metadata.version("roboto")

    state = CLIState(last_checked_version=None)
    if cli_state_file.is_file():
        state = CLIState.parse_file(cli_state_file)
        last_version = state.last_version

    if (
        state.last_checked_version is None
        or version != last_version
        or state.out_of_date is None
        or state.out_of_date is True
        or (utcnow() - datetime.timedelta(hours=1)) > state.last_checked_version
    ):
        http = HttpClient()

        releases = http.get(url="https://pypi.org/pypi/roboto/json").from_json(
            json_path=["releases"]
        )
        versions = list(releases.keys())
        versions.sort(key=StrictVersion)
        latest = versions[-1]

        state.last_checked_version = utcnow()
        state.last_version = version
        state.out_of_date = version != latest

        cli_state_file.write_text(state.json())

        suppress_message = (
            os.getenv("ROBOTO_CLI_SUPPRESS_UPGRADE_PROMPT", "false").lower() != "false"
        )

        if state.out_of_date and not suppress_message:
            notice = f"{AnsiColor.BLUE}[notice]{AnsiColor.END}"
            print(
                f"\n{notice} A new release of roboto is available: "
                + f"{AnsiColor.RED + version + AnsiColor.END} -> {AnsiColor.GREEN + latest + AnsiColor.END}\n"
                + f"{notice} To update, run: {AnsiColor.GREEN}pip install --upgrade roboto{AnsiColor.END}",
                file=sys.stderr,
            )
