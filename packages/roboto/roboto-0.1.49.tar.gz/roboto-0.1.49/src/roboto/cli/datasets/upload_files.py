#  Copyright (c) 2023 Roboto Technologies, Inc.
import argparse
import pathlib

from ...domain.datasets import Dataset
from ..command import (
    ExistingPathlibPath,
    RobotoCommand,
)
from ..common_args import add_org_arg
from ..context import CLIContext
from .shared_helpdoc import DATASET_ID_HELP


def upload_files(args, context: CLIContext, parser: argparse.ArgumentParser):
    path: pathlib.Path = args.path
    if args.exclude is not None and not path.is_dir():
        parser.error(
            "Exclude filters are only supported for directory uploads, not single files."
        )
    if args.key is not None and path.is_dir():
        parser.error(
            "Key overrides are only supported for single file uploads, now directories."
        )

    dataset = Dataset.from_id(
        args.dataset_id, context.datasets, context.files, org_id=args.org
    )

    if path.is_dir():
        dataset.upload_directory(directory_path=path, exclude_patterns=args.exclude)
    else:
        key = path.name if args.key is None else args.key
        dataset.upload_file(path, key)


def upload_files_setup_parser(parser):
    parser.add_argument(
        "-d", "--dataset-id", type=str, required=True, help=DATASET_ID_HELP
    )
    parser.add_argument(
        "-k",
        "--key",
        type=str,
        help="A key to alias a file to when storing it to a dataset. Does nothing for directories.",
    )
    parser.add_argument(
        "-p",
        "--path",
        type=ExistingPathlibPath,
        required=True,
        help="The path to a file or directory to upload.",
    )
    parser.add_argument(
        "-x",
        "--exclude",
        type=str,
        nargs="*",
        help="Zero or more exclude filters (if path points to a directory)",
    )
    add_org_arg(parser)


upload_files_command = RobotoCommand(
    name="upload-files",
    logic=upload_files,
    setup_parser=upload_files_setup_parser,
    command_kwargs={"help": "Uploads a file or directory to a specific dataset."},
)
