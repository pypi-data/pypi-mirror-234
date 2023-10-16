#  Copyright (c) 2023 Roboto Technologies, Inc.
import argparse

from ...domain.actions import Invocation
from ..command import RobotoCommand
from ..common_args import add_org_arg
from ..context import CLIContext


def cancel(
    args: argparse.Namespace, context: CLIContext, parser: argparse.ArgumentParser
) -> None:
    invocation = Invocation.from_id(
        args.invocation_id,
        invocation_delegate=context.invocations,
        org_id=args.org,
    )
    invocation.cancel()
    print("Invocation cancelled.")
    return


def cancel_parser(parser: argparse.ArgumentParser):
    parser.add_argument("invocation_id")
    add_org_arg(parser=parser)


cancel_command = RobotoCommand(
    name="cancel",
    logic=cancel,
    setup_parser=cancel_parser,
    command_kwargs={"help": "Cancel invocation."},
)
