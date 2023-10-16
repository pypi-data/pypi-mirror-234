import collections.abc
import json
import typing

import pydantic


def safe_dict_drill(
    target: dict[typing.Any, typing.Any],
    keys: list[typing.Any],
    case_insensitive: bool = False,
) -> typing.Any:
    value = target

    for key in keys:
        if type(value) is not dict:
            return None

        if case_insensitive:
            value = case_insensitive_get(value, key)
        else:
            value = value.get(key, None)

        if value is None:
            return None

    return value


def case_insensitive_get(
    target: dict[str, typing.Any], key: str, default: typing.Any = None
) -> typing.Any:
    matches = list(filter(lambda k: k.lower() == key.lower(), target.keys()))
    n_matches = len(matches)
    if n_matches == 0:
        return default
    elif n_matches == 1:
        return target[matches[0]]
    else:
        raise ValueError(
            f"{n_matches} equivalent case-insensitive keys found for {key}"
        )


def pydantic_jsonable_dict(
    model: pydantic.BaseModel, exclude_none=False, exclude_unset=False
) -> dict:
    return json.loads(
        model.json(exclude_none=exclude_none, exclude_unset=exclude_unset)
    )


def pydantic_jsonable_dicts(
    models: collections.abc.Iterable, exclude_none=False, exclude_unset=False
) -> list[dict]:
    return [
        pydantic_jsonable_dict(model, exclude_none, exclude_unset) for model in models
    ]


def pydantic_jsonable_dict_map(
    models: collections.abc.Mapping, exclude_none=False, exclude_unset=False
) -> dict:
    dict_map = {}

    for key, value in models.items():
        dict_map[key] = pydantic_jsonable_dict(value, exclude_none, exclude_unset)

    return dict_map
