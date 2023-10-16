#  Copyright (c) 2023 Roboto Technologies, Inc.

import argparse

from ...domain.collections import Collection
from ..command import RobotoCommand
from ..common_args import add_org_arg
from ..context import CLIContext
from .shared_helpdoc import COLLECTION_ID_HELP


def show(args, context: CLIContext, parser: argparse.ArgumentParser):
    collection = Collection.from_id(
        collection_id=args.collection_id,
        org_id=args.org,
        delegate=context.collections,
    )
    for change in collection.changes(
        from_version=args.from_version, to_version=args.to_version
    ):
        print(change.json())


def show_setup_parser(parser):
    parser.add_argument("collection_id", type=str, help=COLLECTION_ID_HELP)
    parser.add_argument(
        "--from-version",
        type=int,
        required=False,
        help="A collection version to use as the starting point in change-set listing. Defaults to initial.",
    )
    parser.add_argument(
        "--to-version",
        type=int,
        required=False,
        help="A collection version to use as the end point in change-set listing. Defaults to latest.",
    )
    add_org_arg(parser)


changes_command = RobotoCommand(
    name="changelog",
    logic=show,
    setup_parser=show_setup_parser,
    command_kwargs={
        "help": "Provides a changelog for the revisions of a given collection."
    },
)
