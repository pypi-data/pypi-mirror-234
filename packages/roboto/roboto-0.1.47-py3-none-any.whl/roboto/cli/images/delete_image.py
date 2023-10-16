#  Copyright (c) 2023 Roboto Technologies, Inc.
import argparse

from ...image_registry import ImageRegistry
from ..command import RobotoCommand
from ..common_args import add_org_arg
from ..context import CLIContext


def delete_image(
    args: argparse.Namespace, context: CLIContext, parser: argparse.ArgumentParser
) -> None:
    image_registry = ImageRegistry(
        context.roboto_service_base_url,
        context.http,
    )
    image_registry.delete_image(args.remote_image, org_id=args.org)


def delete_image_parser(parser: argparse.ArgumentParser) -> None:
    add_org_arg(parser)

    parser.add_argument(
        "remote_image",
        action="store",
        help="Specify the remote image to delete, in the format '<repository>:<tag>'.",
    )


delete_image_command = RobotoCommand(
    name="delete-image",
    logic=delete_image,
    setup_parser=delete_image_parser,
    command_kwargs={
        "help": (
            "Delete a container image hosted in Roboto's image registry. "
            "Requires Docker CLI."
        )
    },
)
