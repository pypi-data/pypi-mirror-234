#  Copyright (c) 2023 Roboto Technologies, Inc.
import argparse
import time
from typing import Any, Optional

from ...domain.actions import Invocation
from ..command import RobotoCommand
from ..common_args import add_org_arg
from ..context import CLIContext


def get_logs(
    args: argparse.Namespace, context: CLIContext, parser: argparse.ArgumentParser
) -> None:
    invocation = Invocation.from_id(
        args.invocation_id,
        invocation_delegate=context.invocations,
        org_id=args.org,
    )

    process_decorator = "=" * 10
    last_log = None
    suppress = False
    for log_record in invocation.get_logs():
        if last_log is None:
            print(f"{process_decorator} {log_record.process.value} {process_decorator}")
        else:
            if suppress and log_record.log_id != last_log.log_id:
                # `last_record` was the last partial message from its group--print it
                suppress = False
                print(last_log.log)

            if last_log.process != log_record.process:
                print()  # Newline separate process output
                print(
                    f"{process_decorator} {log_record.process.value} {process_decorator}"
                )

            if log_record.is_partial:
                # Wait until we know we've seen the last partial message from this group
                suppress = True

        if not suppress:
            print(log_record.log)

        last_log = log_record


def stream_logs(
    args: argparse.Namespace, context: CLIContext, parser: argparse.ArgumentParser
) -> None:
    invocation = Invocation.from_id(
        args.invocation_id,
        invocation_delegate=context.invocations,
        org_id=args.org,
    )

    last_read: Optional[Any] = None
    wait_msg = ""
    last_log = None
    suppress = False
    process_decorator = "=" * 10
    try:
        while True:
            try:
                log_record_generator = invocation.stream_logs(last_read)
                while True:
                    log_record = next(log_record_generator)
                    if wait_msg:
                        # Clear wait message
                        print("\r", " " * len(wait_msg), end="\r", flush=True)
                        wait_msg = ""

                    if last_log is None:
                        print(
                            f"{process_decorator} {log_record.process.value} {process_decorator}"
                        )
                    else:
                        if suppress and log_record.log_id != last_log.log_id:
                            # `last_record` was the last partial message from its group--print it
                            suppress = False
                            print(last_log.log)

                        if last_log.process != log_record.process:
                            print()  # Newline separate process output
                            print(
                                f"{process_decorator} {log_record.process.value} {process_decorator}"
                            )

                        if log_record.is_partial:
                            # Wait until we know we've seen the last partial message from this group
                            suppress = True

                    if not suppress:
                        print(log_record.log)

                    last_log = log_record
            except StopIteration as stop:
                if invocation.reached_terminal_status:
                    break

                if not wait_msg:
                    wait_msg = "Waiting for logs..."
                    print(wait_msg, end="", flush=True)

                last_read = stop.value
                time.sleep(2)
                invocation.refresh()
    except KeyboardInterrupt:
        pass  # Swallow

    if wait_msg:
        print("\r", " " * len(wait_msg), end="\r", flush=True)


def main(
    args: argparse.Namespace, context: CLIContext, parser: argparse.ArgumentParser
) -> None:
    if args.tail:
        stream_logs(args, context, parser)
    else:
        get_logs(args, context, parser)


def get_logs_parser(parser: argparse.ArgumentParser):
    parser.add_argument("invocation_id")
    parser.add_argument("--tail", required=False, action="store_true")
    add_org_arg(parser=parser)


get_logs_command = RobotoCommand(
    name="logs",
    logic=main,
    setup_parser=get_logs_parser,
    command_kwargs={"help": "Get invocation logs."},
)
