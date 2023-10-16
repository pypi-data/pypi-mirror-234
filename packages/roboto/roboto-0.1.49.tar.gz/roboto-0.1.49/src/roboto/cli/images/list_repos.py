#  Copyright (c) 2023 Roboto Technologies, Inc.
import argparse
import json

from ...image_registry import ImageRegistry
from ..command import RobotoCommand
from ..common_args import add_org_arg
from ..context import CLIContext


def list_repos(
    args: argparse.Namespace, context: CLIContext, parser: argparse.ArgumentParser
) -> None:
    image_registry = ImageRegistry(
        context.roboto_service_base_url,
        context.http,
    )
    paginated_results = image_registry.list_repositories(org_id=args.org)
    while True:
        for repo in paginated_results.items:
            print(json.dumps(repo.dict(), indent=2))
        if paginated_results.next_token:
            paginated_results = image_registry.list_repositories(
                page_token=paginated_results.next_token, org_id=args.org
            )
        else:
            break


def list_repos_parser(parser: argparse.ArgumentParser) -> None:
    add_org_arg(parser)


ls_repos_command = RobotoCommand(
    name="ls-repos",
    logic=list_repos,
    setup_parser=list_repos_parser,
    command_kwargs={
        "help": "List image repositories hosted in Roboto's image registry."
    },
)
