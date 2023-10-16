#  Copyright (c) 2023 Roboto Technologies, Inc.

"""
SerDe: Serialization + Deserialization

This module contains utility functions for common serialization and deserialization scenarios used
throughout the Roboto python codebase.
"""

from .dicts import (
    case_insensitive_get,
    pydantic_jsonable_dict,
    pydantic_jsonable_dict_map,
    pydantic_jsonable_dicts,
    safe_dict_drill,
)
from .paths import (
    git_paths_match,
    git_paths_to_spec,
)

__all__ = [
    "pydantic_jsonable_dict",
    "pydantic_jsonable_dicts",
    "pydantic_jsonable_dict_map",
    "safe_dict_drill",
    "case_insensitive_get",
    "git_paths_to_spec",
    "git_paths_match",
]
