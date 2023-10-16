#  Copyright (c) 2023 Roboto Technologies, Inc.
import argparse
import pathlib

from ...domain.datasets import Dataset
from ..command import RobotoCommand
from ..common_args import add_org_arg
from ..context import CLIContext
from .shared_helpdoc import DATASET_ID_HELP


def download_files(args, context: CLIContext, parser: argparse.ArgumentParser):
    record = Dataset.from_id(
        args.dataset_id, context.datasets, context.files, org_id=args.org
    )

    record.download_files(
        out_path=args.path, include_patterns=args.include, exclude_patterns=args.exclude
    )


def download_files_setup_parser(parser):
    parser.add_argument(
        "-d", "--dataset-id", type=str, required=True, help=DATASET_ID_HELP
    )
    parser.add_argument(
        "-p",
        "--path",
        type=pathlib.Path,
        required=True,
        help="The download destination for this operation.",
    )
    parser.add_argument(
        "-i",
        "--include",
        type=str,
        nargs="*",
        help="Zero or more include filters (if path points to a directory)",
    )
    parser.add_argument(
        "-x",
        "--exclude",
        type=str,
        nargs="*",
        help="Zero or more exclude filters (if path points to a directory)",
    )
    add_org_arg(parser)


download_files_command = RobotoCommand(
    name="download-files",
    logic=download_files,
    setup_parser=download_files_setup_parser,
    command_kwargs={"help": "Downloads a file or directory from a specific dataset."},
)
