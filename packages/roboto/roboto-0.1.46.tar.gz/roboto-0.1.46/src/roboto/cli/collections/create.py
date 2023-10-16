#  Copyright (c) 2023 Roboto Technologies, Inc.

import argparse

from ...domain.collections import (
    Collection,
    CollectionResourceRef,
    CollectionResourceType,
)
from ..command import RobotoCommand
from ..common_args import add_org_arg
from ..context import CLIContext


def create(args, context: CLIContext, parser: argparse.ArgumentParser):
    collection = Collection.create(
        name=args.name,
        description=args.description,
        tags=args.tag,
        resources=None
        if args.dataset_id is None
        else [
            CollectionResourceRef(
                resource_type=CollectionResourceType.Dataset, resource_id=dataset_id
            )
            for dataset_id in args.dataset_id
        ],
        org_id=args.org,
        delegate=context.collections,
    )
    print(collection.record.json())


def create_setup_parser(parser):
    parser.add_argument(
        "--name",
        type=str,
        help="A human-readable name for this collection. "
        + "Does not need to be unique.",
    )
    parser.add_argument(
        "--description", type=str, help="Information about what's in this collection"
    )
    parser.add_argument(
        "--dataset-id",
        nargs="*",
        help="Initial datasets to add to this collection.",
        action="extend",
    )
    parser.add_argument(
        "--tag",
        type=str,
        nargs="*",
        help="Tags that make it easier to discover this collection.",
        action="extend",
    )
    add_org_arg(parser)


create_command = RobotoCommand(
    name="create",
    logic=create,
    setup_parser=create_setup_parser,
    command_kwargs={"help": "Creates a new collection."},
)
