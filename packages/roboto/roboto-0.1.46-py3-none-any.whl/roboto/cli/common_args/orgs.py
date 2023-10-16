#  Copyright (c) 2023 Roboto Technologies, Inc.

import argparse
import os

ORG_ARG_HELP = (
    "The calling organization ID. Gets set implicitly if in a single org. "
    + "The `ROBOTO_ORG_ID` environment variable can be set to control the default value."
)

DEFAULT_ORG_ID = os.getenv("ROBOTO_ORG_ID")


def add_org_arg(parser: argparse.ArgumentParser, arg_help: str = ORG_ARG_HELP):
    parser.add_argument(
        "--org", required=False, type=str, help=arg_help, default=DEFAULT_ORG_ID
    )
