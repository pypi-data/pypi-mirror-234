#  Copyright (c) 2023 Roboto Technologies, Inc.
import argparse
import json
import time

from ...domain.actions import (
    Invocation,
    InvocationStatus,
)
from ..command import RobotoCommand
from ..common_args import add_org_arg
from ..context import CLIContext


def status(
    args: argparse.Namespace, context: CLIContext, parser: argparse.ArgumentParser
) -> None:
    if not args.tail:
        invocation = Invocation.from_id(
            args.invocation_id,
            invocation_delegate=context.invocations,
            org_id=args.org,
        )
        print(
            json.dumps(
                [
                    status_record.to_presentable_dict()
                    for status_record in invocation.status_log
                ],
                indent=4,
            )
        )
        return

    printed: set[InvocationStatus] = set()
    invocation = Invocation.from_id(
        args.invocation_id,
        invocation_delegate=context.invocations,
        org_id=args.org,
    )
    try:
        while True:
            status_records_to_print = [
                status_record
                for status_record in invocation.status_log
                if status_record.status not in printed
            ]
            if status_records_to_print:
                for status_record in status_records_to_print:
                    printed.add(status_record.status)
                    print(json.dumps(status_record.to_presentable_dict(), indent=4))

            if invocation.reached_terminal_status:
                break

            time.sleep(1)
            invocation.refresh()
    except KeyboardInterrupt:
        pass  # Swallow


def status_parser(parser: argparse.ArgumentParser):
    parser.add_argument("invocation_id")
    parser.add_argument("--tail", required=False, action="store_true")
    add_org_arg(parser=parser)


status_command = RobotoCommand(
    name="status",
    logic=status,
    setup_parser=status_parser,
    command_kwargs={"help": "Get invocation status."},
)
