import enum
import sys
import typing


class AnsiColor(str, enum.Enum):
    RED = "\033[0;31m"
    GREEN = "\033[0;32m"
    BLUE = "\033[0;34m"
    END = "\033[0m"


def print_error_and_exit(msg: typing.Union[str, list[str]]) -> typing.NoReturn:
    if isinstance(msg, list):
        for line in msg:
            print(f"{AnsiColor.RED}[error]{AnsiColor.END} {line}", file=sys.stderr)
    else:
        print(f"{AnsiColor.RED}[error]{AnsiColor.END} {msg}", file=sys.stderr)
    sys.exit(1)
