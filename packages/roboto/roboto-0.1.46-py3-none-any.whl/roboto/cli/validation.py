import contextlib

import pydantic

from .terminal import print_error_and_exit


class print_validation_error_and_exit(contextlib.AbstractContextManager):
    """
    Context manager to catch Pydantic validation errors and print the first error neatly to stderr.
    """

    def __enter__(self):
        pass

    def __exit__(self, exctype, excinst, exctb):
        if exctype is None:
            return

        if issubclass(exctype, pydantic.ValidationError):
            first_error, *_rest = excinst.errors()
            msg = first_error.get("msg")
            loc = first_error.get("loc", tuple())
            if loc:
                path_to_error = ".".join([str(key_path) for key_path in loc])
                msg = f"'{path_to_error}' {msg}"

            error_msg = ["Error parsing Action config file"]
            if msg:
                error_msg.append(msg)

            print_error_and_exit(error_msg)

        return False
