#  Copyright (c) 2023 Roboto Technologies, Inc.
import argparse
import json
import typing

from ...domain import actions
from ...sentinels import NotSet
from ...updates import MetadataChangeset
from ..command import (
    KeyValuePairsAction,
    RobotoCommand,
)
from ..common_args import (
    ActionParameterArg,
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

null = object()


def update(
    args: argparse.Namespace, context: CLIContext, parser: argparse.ArgumentParser
) -> None:
    action = actions.Action.from_name(
        name=args.action,
        action_delegate=context.actions,
        invocation_delegate=context.invocations,
        org_id=args.org,
    )
    updates: dict[str, typing.Any] = dict()
    if args.description is null:
        updates["description"] = None
    elif args.description != NotSet:
        updates["description"] = args.description if args.description else None

    if args.image != NotSet:
        stripped = args.image.strip()
        if not stripped:
            raise ValueError(
                "image can neither be unset nor set to an empty (or whitespace-only) string"
            )
        updates["uri"] = stripped
    with print_validation_error_and_exit():
        parameter_changeset = actions.ActionParameterChangeset(
            put_parameters=args.put_parameters if args.put_parameters else [],
            remove_parameters=args.remove_parameters if args.remove_parameters else [],
        )
        if not parameter_changeset.is_empty():
            updates["parameter_changeset"] = parameter_changeset

        metadata_changeset = MetadataChangeset(
            put_tags=args.put_tags,
            remove_tags=args.remove_tags,
            put_fields=args.put_metadata,
            remove_fields=args.remove_metadata,
        )
        if not metadata_changeset.is_empty():
            updates["metadata_changeset"] = metadata_changeset

    compute_requirements = parse_compute_requirements(args, action.compute_requirements)
    if compute_requirements:
        updates["compute_requirements"] = compute_requirements

    container_parameters = parse_container_overrides(args, action.container_parameters)
    if container_parameters:
        updates["container_parameters"] = container_parameters

    if not updates:
        print_error_and_exit("No updates specified. Nothing to do.")

    action.update(**updates)

    print(f"Successfully updated action '{action.name}'. Record: ")
    print(json.dumps(action.to_dict(), indent=4))


def update_parser(parser: argparse.ArgumentParser):
    parser.add_argument(
        "action",
        metavar="action_reference: <action_name>",
        help="Exact name of action to update.",
    )
    parser.add_argument(
        "--description",
        required=False,
        action="store",
        type=lambda s: s if s != "null" else null,
        default=NotSet,
        help="Optional description of action. Specify 'null' to unset existing description.",
    )
    parser.add_argument(
        "--image",
        required=False,
        action="store",
        dest="image",
        type=str,
        default=NotSet,
        help="Register a Docker image with this action. Can neither be unset nor set an empty string.",
    )
    parser.add_argument(
        "--put-parameter",
        dest="put_parameters",
        required=False,
        metavar=ActionParameterArg.METAVAR,
        nargs="*",
        action=ActionParameterArg,
        help=(
            "Add parameter(s) or overwrite existing parameter(s) with the same name. "
            "Argument values must be wrapped in quotes. E.g.: "
            "--put-parameter 'name=my_param|required=true|description=My description of my_param'"
        ),
    )
    parser.add_argument(
        "--remove-parameter",
        dest="remove_parameters",
        required=False,
        metavar="PARAMETER_NAME",
        nargs="*",
        help="Remove parameter(s) with the given name(s).",
    )
    parser.add_argument(
        "--put-tags",
        help="Add each tag in this sequence if it doesn't exist",
        nargs="*",  # 0 or more
    )

    parser.add_argument(
        "--remove-tags",
        help="Remove each tag in this sequence if it exists",
        nargs="*",  # 0 or more
    )

    parser.add_argument(
        "--put-metadata",
        required=False,
        metavar="KEY_PATH=VALUE",
        nargs="*",
        action=KeyValuePairsAction,
        help=(
            "Zero or more 'key_path=value' formatted pairs. "
            "An attempt is made to parse `value` as JSON; if this fails, `value` is stored as a string. "
            "If `key_path` already exists, existing value will be overwritten. "
            "Dot notation is supported for nested keys. "
            "Examples: "
            "--put-metadata 'key1=value1' 'key2.subkey1=value2' 'key3.sublist1=[\"a\",\"b\",\"c\"]'"  # noqa: E501
        ),
    )

    parser.add_argument(
        "--remove-metadata",
        required=False,
        metavar="KEY_PATH",
        nargs="*",
        help=(
            "Remove each key from dataset metadata if it exists. "
            "Dot notation is supported for nested keys. E.g.: --remove-metadata key1 key2.subkey3"
        ),
    )
    add_org_arg(parser=parser)
    add_compute_requirements_args(parser)
    add_container_parameters_args(parser)


update_command = RobotoCommand(
    name="update",
    logic=update,
    setup_parser=update_parser,
    command_kwargs={"help": "Update an existing action."},
)
