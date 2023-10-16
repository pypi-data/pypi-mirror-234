#  Copyright (c) 2023 Roboto Technologies, Inc.

import argparse

from ...domain.collections import Collection
from ..command import RobotoCommand
from ..common_args import add_org_arg
from ..context import CLIContext


def list(args, context: CLIContext, parser: argparse.ArgumentParser):
    for collection in Collection.list_all(
        org_id=args.org, delegate=context.collections
    ):
        print(collection.record.json())


list_command = RobotoCommand(
    name="list",
    logic=list,
    setup_parser=add_org_arg,
    command_kwargs={"help": "Lists existing collections."},
)
