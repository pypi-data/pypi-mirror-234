#  Copyright (c) 2023 Roboto Technologies, Inc.

import argparse
import typing

from roboto.sentinels import (
    NotSet,
    NotSetType,
    value_or_not_set,
)

from ...domain.collections import (
    Collection,
    CollectionResourceRef,
    CollectionResourceType,
)
from ..command import RobotoCommand
from ..common_args import add_org_arg
from ..context import CLIContext
from .shared_helpdoc import COLLECTION_ID_HELP


def update(args, context: CLIContext, parser: argparse.ArgumentParser):
    collection = Collection.from_id(
        collection_id=args.collection_id,
        org_id=args.org,
        delegate=context.collections,
    )

    add_resources: typing.Union[NotSetType, list[CollectionResourceRef]] = (
        NotSet
        if not args.add_dataset_id
        else [
            CollectionResourceRef(
                resource_type=CollectionResourceType.Dataset, resource_id=dataset_id
            )
            for dataset_id in args.add_dataset_id
        ]
    )

    remove_resources: typing.Union[NotSetType, list[CollectionResourceRef]] = (
        NotSet
        if not args.remove_dataset_id
        else [
            CollectionResourceRef(
                resource_type=CollectionResourceType.Dataset, resource_id=dataset_id
            )
            for dataset_id in args.remove_dataset_id
        ]
    )

    collection.update(
        name=value_or_not_set(args.name),
        description=value_or_not_set(args.description),
        add_tags=value_or_not_set(args.add_tag),
        remove_tags=value_or_not_set(args.remove_tag),
        add_resources=add_resources,
        remove_resources=remove_resources,
    )

    print(collection.record.json())


def update_setup_parser(parser):
    parser.add_argument("collection_id", type=str, help=COLLECTION_ID_HELP)
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
        "--add-dataset-id",
        nargs="*",
        help="Datasets to add to this collection.",
        action="extend",
    )
    parser.add_argument(
        "--remove-dataset-id",
        nargs="*",
        help="Datasets to remove from this collection.",
        action="extend",
    )
    parser.add_argument(
        "--add-tag",
        type=str,
        nargs="*",
        help="Tags to add to this collection.",
        action="extend",
    )
    parser.add_argument(
        "--remove-tag",
        type=str,
        nargs="*",
        help="Tags to remove from this collection.",
        action="extend",
    )
    add_org_arg(parser)


update_command = RobotoCommand(
    name="update",
    logic=update,
    setup_parser=update_setup_parser,
    command_kwargs={
        "help": "Updates the resources and metadata of a given collection."
    },
)
