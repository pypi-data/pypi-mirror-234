#  Copyright (c) 2023 Roboto Technologies, Inc.
import argparse
import sys

from ...domain.datasets import Dataset
from ..command import RobotoCommand
from ..common_args import add_org_arg
from ..context import CLIContext
from .shared_helpdoc import DATASET_ID_HELP


def list_files(args, context: CLIContext, parser: argparse.ArgumentParser):
    record = Dataset.from_id(
        args.dataset_id, context.datasets, context.files, org_id=args.org
    )

    for f in record.list_files():
        sys.stdout.write(f"{f.relative_path}\n")


def list_files_setup_parser(parser):
    parser.add_argument(
        "-d", "--dataset-id", type=str, required=True, help=DATASET_ID_HELP
    )
    add_org_arg(parser)


list_files_command = RobotoCommand(
    name="list-files",
    logic=list_files,
    setup_parser=list_files_setup_parser,
    command_kwargs={"help": "Lists files for a specific dataset."},
)
