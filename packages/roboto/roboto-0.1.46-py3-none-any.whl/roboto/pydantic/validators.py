#  Copyright (c) 2023 Roboto Technologies, Inc.


def validate_nonzero_gitpath_specs(value: list[str]) -> list[str]:
    filtered = list(filter(lambda p: p.strip() != "", value))

    if len(value) == 0:
        raise ValueError("Paths must not be empty.")
    elif len(filtered) == 0:
        raise ValueError(
            "Paths must have at least one entry which is not the empty string or just whitespace."
        )

    return value
