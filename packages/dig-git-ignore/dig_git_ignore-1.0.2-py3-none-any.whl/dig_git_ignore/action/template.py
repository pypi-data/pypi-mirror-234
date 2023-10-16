import os.path
from typing import Set
from sys import version_info
from ..constants import GITIGNORE_FILENAME, CONTENT_BLOCK_START


def current() -> Set[str]:
    output: Set[str] = set()
    if not os.path.exists(GITIGNORE_FILENAME):
        return output
    with open(GITIGNORE_FILENAME, mode="r", encoding="utf-8") as file:
        line = file.readline()
        while line:
            if line.startswith(CONTENT_BLOCK_START):
                return set(_remove_suffix(line, "\n").split("/").pop().split(","))
            line = file.readline()
    return output


def _remove_suffix(string: str, suffix: str) -> str:
    if version_info >= (3, 9):
        return string.removesuffix(suffix)
    if string.endswith(suffix):
        return string[: -len(suffix)]
    return string
