#  Copyright (c) 2023 Roboto Technologies, Inc.

from ..command import RobotoCommandSet
from .changes import changes_command
from .create import create_command
from .delete import delete_command
from .list import list_command
from .show import show_command
from .update import update_command

command_set = RobotoCommandSet(
    name="collections",
    help="Curate collections of datasets and other data types.",
    commands=[
        changes_command,
        create_command,
        delete_command,
        list_command,
        show_command,
        update_command,
    ],
)
