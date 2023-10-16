from typing import Set
from pathlib import Path
from io import TextIOWrapper
import os
from ..constants import (
    PROVIDER_URL,
    GITIGNORE_DOWNLOAD,
    GITIGNORE_FILENAME,
    GITIGNORE_TEMP,
    CONTENT_BLOCK_START,
    CONTENT_BLOCK_END,
)
from ..provider import download_gitignore


def update(template: Set[str], url: str = PROVIDER_URL) -> None:
    download_gitignore(Path(GITIGNORE_DOWNLOAD), template, url)
    if not os.path.exists(GITIGNORE_FILENAME):
        # Create empty gitignore
        with open(GITIGNORE_FILENAME, mode="wb"):
            pass

    with open(GITIGNORE_FILENAME, mode="rt", encoding="utf-8") as current:
        with open(GITIGNORE_DOWNLOAD, mode="rt", encoding="utf-8") as downloaded:
            with open(GITIGNORE_TEMP, mode="wt", encoding="utf-8") as new:
                _merge_gitignore(current, downloaded, new)
    os.remove(GITIGNORE_DOWNLOAD)
    os.remove(GITIGNORE_FILENAME)
    os.rename(GITIGNORE_TEMP, GITIGNORE_FILENAME)


def _merge_gitignore(current: TextIOWrapper, downloaded: TextIOWrapper, output: TextIOWrapper) -> None:
    # Copy current gitignore before block start
    line = current.readline()
    while line:
        if line.startswith(CONTENT_BLOCK_START):
            break
        output.write(line)
        line = current.readline()

    # Copy downloaded gitignore block
    line = downloaded.readline()
    while line:
        if line.startswith(CONTENT_BLOCK_END):
            output.write(line)
            break
        output.write(line)
        line = downloaded.readline()

    # Find current gitignore block end
    line = current.readline()
    while line:
        if line.startswith(CONTENT_BLOCK_END):
            line = current.readline()
            break
        line = current.readline()
    # Copy current gitignore remanescent content
    while line:
        output.write(line)
        line = current.readline()
