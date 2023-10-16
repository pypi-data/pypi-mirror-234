#  Copyright (c) 2023 Roboto Technologies, Inc.
import argparse
import shlex
import subprocess
import sys

from ...auth import Permissions
from ...image_registry import ImageRegistry
from ...waiters import TimeoutError, wait_for
from ..command import RobotoCommand
from ..common_args import add_org_arg
from ..context import CLIContext


def push(
    args: argparse.Namespace, context: CLIContext, parser: argparse.ArgumentParser
) -> None:
    inspect_cmd = f"docker image inspect {args.local_image}"
    try:
        subprocess.run(
            shlex.split(inspect_cmd),
            capture_output=True,
            check=True,
            text=True,
        )
    except subprocess.CalledProcessError:
        print(
            f"Could not find locally built image '{args.local_image}'. Is the repository name and tag correct?",
            file=sys.stderr,
        )
        return

    image_registry = ImageRegistry(
        context.roboto_service_base_url,
        context.http,
    )
    parts = args.local_image.split(":")
    if len(parts) == 1:
        repo, tag = parts[0], "latest"
    elif len(parts) == 2:
        repo, tag = parts
    else:
        raise ValueError("Invalid image format. Expected '<repository>:<tag>'.")
    repository = image_registry.create_repository(repo, org_id=args.org)
    credentials = image_registry.get_temporary_credentials(
        repository["repository_uri"], Permissions.ReadWrite, org_id=args.org
    )
    login_cmd = f"docker login --username {credentials.username} --password-stdin {credentials.registry_url}"
    try:
        subprocess.run(
            shlex.split(login_cmd),
            capture_output=True,
            check=True,
            input=credentials.password,
            text=True,
        )
    except subprocess.CalledProcessError as exc:
        print(
            "Failed to set Docker credentials for Roboto's image registry.",
            file=sys.stderr,
        )
        if exc.stdout:
            print(exc.stdout, file=sys.stderr)
        if exc.stderr:
            print(exc.stderr, file=sys.stderr)
        return

    image_uri = f"{repository['repository_uri']}:{tag}"
    tag_cmd = f"docker tag {args.local_image} {image_uri}"
    try:
        subprocess.run(
            shlex.split(tag_cmd),
            capture_output=True,
            check=True,
            text=True,
        )
    except subprocess.CalledProcessError as exc:
        print(
            f"Failed to tag local image '{args.local_image}' as '{image_uri}'.",
            file=sys.stderr,
        )
        if exc.stdout:
            print(exc.stdout, file=sys.stderr)
        if exc.stderr:
            print(exc.stderr, file=sys.stderr)
        return

    push_cmd = f"docker push {image_uri}"
    with subprocess.Popen(
        shlex.split(push_cmd),
        text=True,
    ) as push_proc:
        try:
            push_proc.wait()
        except KeyboardInterrupt:
            push_proc.kill()
            return

    print("Waiting for image to be available...")
    try:
        wait_for(
            image_registry.repository_contains_image,
            args=[repository["repository_name"], tag, args.org],
            interval=lambda iteration: min((2**iteration) / 2, 32),
        )
        print(
            f"Image pushed successfully! You can now use '{image_uri}' in your Roboto Actions."
        )
    except TimeoutError:
        print(
            "Image could not be confirmed as successfully pushed. Try pushing again in a few minutes."
        )
    except KeyboardInterrupt:
        print("")


def push_parser(parser: argparse.ArgumentParser) -> None:
    add_org_arg(parser)

    parser.add_argument(
        "local_image",
        action="store",
        help=(
            "Specify the local image to push, in the format '<repository>:<tag>'. "
            "If no tag is specified, 'latest' is assumed. "
            "Image must exist locally (i.e. 'docker images' must list it)."
        ),
    )


push_command = RobotoCommand(
    name="push",
    logic=push,
    setup_parser=push_parser,
    command_kwargs={
        "help": (
            "Push a local container image into Roboto's image registry. "
            "Requires Docker CLI."
        )
    },
)
