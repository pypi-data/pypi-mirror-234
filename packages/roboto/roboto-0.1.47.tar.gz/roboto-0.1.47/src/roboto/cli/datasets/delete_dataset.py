#  Copyright (c) 2023 Roboto Technologies, Inc.
import argparse

from ...domain.datasets import Dataset
from ..command import RobotoCommand
from ..common_args import add_org_arg
from ..context import CLIContext
from .shared_helpdoc import DATASET_ID_HELP


def delete_dataset(args, context: CLIContext, parser: argparse.ArgumentParser):
    dataset = Dataset.from_id(
        args.dataset_id, context.datasets, context.files, org_id=args.org
    )
    dataset.delete_dataset()
    print(f"Deleted dataset {args.dataset_id}")


def delete_dataset_setup_parser(parser):
    parser.add_argument(
        "-d", "--dataset-id", type=str, required=True, help=DATASET_ID_HELP
    )
    add_org_arg(parser)


delete_dataset_command = RobotoCommand(
    name="delete",
    logic=delete_dataset,
    setup_parser=delete_dataset_setup_parser,
    command_kwargs={"help": "Delete dataset (and all related subresources) by id."},
)
