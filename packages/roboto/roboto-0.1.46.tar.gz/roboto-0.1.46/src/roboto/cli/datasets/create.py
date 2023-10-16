#  Copyright (c) 2023 Roboto Technologies, Inc.
import argparse
import json

from ...domain.datasets import Dataset
from ..command import (
    KeyValuePairsAction,
    RobotoCommand,
)
from ..common_args import add_org_arg
from ..context import CLIContext


def create(args, context: CLIContext, parser: argparse.ArgumentParser):
    dataset = Dataset.create(
        context.datasets,
        context.files,
        metadata=args.metadata,
        tags=args.tag,
        org_id=args.org,
        description=args.description,
    )

    print(json.dumps(dataset.to_dict(), indent=4))


def create_setup_parser(parser):
    parser.add_argument(
        "-m",
        "--metadata",
        metavar="KEY=VALUE",
        nargs="*",
        action=KeyValuePairsAction,
        help="Zero or more 'key=value' format key/value pairs which represent dataset metadata. "
        + "Metadata can be mutated after creation.",
    )
    parser.add_argument(
        "-t",
        "--tag",
        type=str,
        nargs="*",
        help="One or more tags to annotate this dataset. Tags can be modified after creation.",
        action="extend",
    )
    parser.add_argument(
        "-d",
        "--description",
        type=str,
        help="A human readable description of this dataset.",
    )
    add_org_arg(parser=parser)


create_command = RobotoCommand(
    name="create",
    logic=create,
    setup_parser=create_setup_parser,
    command_kwargs={"help": "Creates a new dataset."},
)
