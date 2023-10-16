#  Copyright (c) 2023 Roboto Technologies, Inc.
from typing import Optional

import pathspec


def git_paths_to_spec(paths: list[str]) -> pathspec.PathSpec:
    return pathspec.PathSpec.from_lines(pathspec.patterns.GitWildMatchPattern, paths)


def git_paths_match(
    include_patterns: Optional[list[str]],
    exclude_patterns: Optional[list[str]],
    file: str,
) -> bool:
    # Include patterns are provided, and the file isn't included, ignore it
    if include_patterns is not None:
        if not git_paths_to_spec(include_patterns).match_file(file):
            return False

    # Exclude pattern is provided, and the file is included, ignore it
    if exclude_patterns is not None:
        if git_paths_to_spec(exclude_patterns).match_file(file):
            return False

    return True
