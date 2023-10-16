#  Copyright (c) 2023 Roboto Technologies, Inc.

import argparse

from ...domain.collections import (
    Collection,
    CollectionContentMode,
)
from ..command import RobotoCommand
from ..common_args import add_org_arg
from ..context import CLIContext
from .shared_helpdoc import (
    COLLECTION_ID_HELP,
    COLLECTION_VERSION_HELP,
    CONTENT_MODE_HELP,
)


def show(args, context: CLIContext, parser: argparse.ArgumentParser):
    collection = Collection.from_id(
        collection_id=args.collection_id,
        version=args.collection_version,
        org_id=args.org,
        delegate=context.collections,
        content_mode=args.content_mode,
    )
    print(collection.record.json())


def show_setup_parser(parser):
    parser.add_argument("collection_id", type=str, help=COLLECTION_ID_HELP)
    parser.add_argument(
        "-v",
        "--collection-version",
        type=int,
        required=False,
        help=COLLECTION_VERSION_HELP,
    )
    parser.add_argument(
        "--content-mode",
        type=str,
        choices=[mode.value for mode in CollectionContentMode],
        help=CONTENT_MODE_HELP,
        default=CollectionContentMode.References.value,
    )
    add_org_arg(parser)


show_command = RobotoCommand(
    name="show",
    logic=show,
    setup_parser=show_setup_parser,
    command_kwargs={"help": "Show information about a specific collection."},
)
