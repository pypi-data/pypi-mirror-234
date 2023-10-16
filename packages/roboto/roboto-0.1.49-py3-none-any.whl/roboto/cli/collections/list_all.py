#  Copyright (c) 2023 Roboto Technologies, Inc.

import argparse

from ...domain.collections import (
    Collection,
    CollectionContentMode,
)
from ..command import RobotoCommand
from ..common_args import add_org_arg
from ..context import CLIContext
from .shared_helpdoc import CONTENT_MODE_HELP


def list_all(args, context: CLIContext, parser: argparse.ArgumentParser):
    for collection in Collection.list_all(
        org_id=args.org, delegate=context.collections, content_mode=args.content_mode
    ):
        print(collection.record.json())


def list_all_setup_parser(parser: argparse.ArgumentParser):
    parser.add_argument(
        "--content-mode",
        type=str,
        choices=[mode.value for mode in CollectionContentMode],
        help=CONTENT_MODE_HELP,
        default=CollectionContentMode.References.value,
    )
    add_org_arg(parser)


list_all_command = RobotoCommand(
    name="list-all",
    logic=list_all,
    setup_parser=list_all_setup_parser,
    command_kwargs={"help": "Lists all collections created for a given org."},
)
