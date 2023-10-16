#  Copyright (c) 2023 Roboto Technologies, Inc.
import argparse
import json
import pathlib
import typing

from ...domain.actions import Action
from ..command import (
    KeyValuePairsAction,
    RobotoCommand,
)
from ..common_args import (
    ActionParameterArg,
    add_action_reference_arg,
    add_compute_requirements_args,
    add_container_parameters_args,
    add_org_arg,
    parse_compute_requirements,
    parse_container_overrides,
)
from ..context import CLIContext
from ..terminal import print_error_and_exit
from ..validation import (
    print_validation_error_and_exit,
)
from .action_config import ActionConfig


def create(
    args: argparse.Namespace, context: CLIContext, parser: argparse.ArgumentParser
) -> None:
    config: typing.Optional[ActionConfig] = None
    if args.action_config_file:
        with print_validation_error_and_exit():
            if not args.action_config_file.exists():
                print_error_and_exit(
                    f"Action config file '{args.action_config_file}' does not exist."
                )
            config = ActionConfig.parse_file(args.action_config_file)

    default_compute_reqs_from_file = config.compute_requirements if config else None
    compute_requirements = parse_compute_requirements(
        args, defaults=default_compute_reqs_from_file
    )

    default_container_parameters_from_file = (
        config.container_parameters if config else None
    )
    container_parameters = parse_container_overrides(
        args, defaults=default_container_parameters_from_file
    )

    metadata = config.metadata if config else dict()
    if args.metadata:
        metadata.update(args.metadata)

    tags = config.tags if config else list()
    if args.tag:
        tags.extend(args.tag)

    parameters = config.parameters if config else list()
    if args.parameter:
        cli_param_names = {param.name for param in args.parameter}
        # replace any existing parameters with the same name
        parameters = [
            param for param in parameters if param.name not in cli_param_names
        ]
        parameters.extend(args.parameter)

    if not args.name and not config:
        print_error_and_exit(
            "Action name is required. Please specify either the `--name` CLI argument or the `name` property in your "
            "Action config file.",
        )

    config_params = {
        "name": args.name,
        "description": args.description,
        "inherits": args.inherits_from,
        "compute_requirements": compute_requirements,
        "container_parameters": container_parameters,
        "metadata": metadata,
        "parameters": args.parameter,
        "tags": tags,
        "image_uri": args.image,
    }
    config_params = {k: v for k, v in config_params.items() if v is not None}

    with print_validation_error_and_exit():
        config_with_overrides = (
            ActionConfig.parse_obj(config_params)
            if config is None
            else config.copy(update=config_params)
        )

    image_uri = None
    if config_with_overrides.docker_config:
        # Build docker image and push it to Roboto's Docker register
        print_error_and_exit(
            [
                "Support for building and pushing Docker images as part of Action creation is forthcoming.",
                "For now, please use the `docker` CLI to build and tag your image, and use `roboto images push` "
                "to push it to Roboto's Docker registry.",
                "Finally, use either the `--image` CLI argument or the `image_uri` property in your Action config file "
                "to associate your Action with the Docker image you just pushed.",
            ]
        )
    else:
        image_uri = config_with_overrides.image_uri

    action = Action.create(
        name=config_with_overrides.name,
        parameters=config_with_overrides.parameters,
        uri=image_uri,
        inherits=config_with_overrides.inherits,
        description=config_with_overrides.description,
        compute_requirements=config_with_overrides.compute_requirements,
        container_parameters=config_with_overrides.container_parameters,
        metadata=config_with_overrides.metadata,
        tags=config_with_overrides.tags,
        action_delegate=context.actions,
        invocation_delegate=context.invocations,
        org_id=args.org,
    )

    print(f"Successfully created action '{action.name}'. Record: ")
    print(json.dumps(action.to_dict(), indent=4))


def create_parser(parser: argparse.ArgumentParser):
    parser.add_argument(
        "--from-file",
        type=pathlib.Path,
        action="store",
        dest="action_config_file",
        help=(
            "Path to a file containing Action configuration. "
            "Other CLI arguments specified will override the values in the config file. "
        ),
    )
    parser.add_argument(
        "--name",
        required=False,
        action="store",
        help=(
            "Name of the action. Not modifiable after creation. "
            "An action is considered unique by its (name, docker_image_name, docker_image_tag) tuple."
        ),
    )

    parser.add_argument(
        "--description",
        required=False,
        action="store",
        help="Optional description of action. Modifiable after creation.",
    )
    add_action_reference_arg(
        parser=parser,
        arg_name="inherits_from",
        arg_help=(
            "Partially or fully qualified reference to action from which to inherit configuration. "
            "Inheriting from another action is mutually exclusive with specifying a container image (--image), "
            "entrypoint (--entrypoint), command (--command), working directory (--workdir), env vars (--env), "
            "or parameter(s) (--parameter). "
        ),
        positional=False,
        required=False,
    )
    parser.add_argument(
        "--image",
        required=False,
        action="store",
        dest="image",
        help="Associate a Docker image with this action. Modifiable after creation.",
    )
    parser.add_argument(
        "--parameter",
        required=False,
        metavar=ActionParameterArg.METAVAR,
        nargs="*",
        action=ActionParameterArg,
        help=(
            "Zero or more parameters (space-separated) accepted by this action. "
            "'name' is the only required attribute. "
            "'default' values, if provided, are JSON parsed. "
            "This argument can be specified multiple times. "
            "Parameters can be modified after creation. "
            "Argument values must be wrapped in quotes. E.g.: "
            "--put-parameter 'name=my_param|required=true|description=My description of my_param'"
        ),
    )
    parser.add_argument(
        "--metadata",
        required=False,
        metavar="KEY=VALUE",
        nargs="*",
        action=KeyValuePairsAction,
        help=(
            "Zero or more 'key=value' format key/value pairs which represent action metadata. "
            "`value` is parsed as JSON. "
            "Metadata can be modified after creation."
        ),
    )
    parser.add_argument(
        "--tag",
        required=False,
        type=str,
        nargs="*",
        help="One or more tags to annotate this action. Modifiable after creation.",
        action="extend",
    )
    add_org_arg(parser=parser)

    add_compute_requirements_args(parser)
    add_container_parameters_args(parser)


create_command = RobotoCommand(
    name="create",
    logic=create,
    setup_parser=create_parser,
    command_kwargs={"help": "Create a new action."},
)
