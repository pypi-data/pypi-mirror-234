#  Copyright (c) 2023 Roboto Technologies, Inc.
import argparse

from ...domain.datasets import Dataset
from ..command import RobotoCommand
from ..common_args import add_org_arg
from ..context import CLIContext
from .shared_helpdoc import DATASET_ID_HELP


def delete_files(args, context: CLIContext, parser: argparse.ArgumentParser):
    dataset = Dataset.from_id(
        args.dataset_id, context.datasets, context.files, org_id=args.org
    )

    dataset.delete_files(include_patterns=args.include, exclude_patterns=args.exclude)


def delete_files_setup_parser(parser):
    parser.add_argument(
        "-d", "--dataset-id", type=str, required=True, help=DATASET_ID_HELP
    )
    parser.add_argument(
        "-i",
        "--include",
        type=str,
        nargs="*",
        help="Zero or more include filters",
    )
    parser.add_argument(
        "-x",
        "--exclude",
        type=str,
        nargs="*",
        help="Zero or more exclude filters",
    )
    add_org_arg(parser)


delete_files_command = RobotoCommand(
    name="delete-files",
    logic=delete_files,
    setup_parser=delete_files_setup_parser,
    command_kwargs={"help": "Delete file(s) from a specific dataset."},
)
