#  Copyright (c) 2023 Roboto Technologies, Inc.
import argparse
import json

from ...domain.datasets import Dataset
from ..command import RobotoCommand
from ..common_args import add_org_arg
from ..context import CLIContext
from .shared_helpdoc import DATASET_ID_HELP


def show(args, context: CLIContext, parser: argparse.ArgumentParser):
    record = Dataset.from_id(
        args.dataset_id, context.datasets, context.files, org_id=args.org
    )
    print(json.dumps(record.to_dict(), indent=4))


def show_setup_parser(parser):
    parser.add_argument(
        "-d", "--dataset-id", type=str, required=True, help=DATASET_ID_HELP
    )
    add_org_arg(parser)


show_command = RobotoCommand(
    name="show",
    logic=show,
    setup_parser=show_setup_parser,
    command_kwargs={"help": "Show information about a specific dataset."},
)
