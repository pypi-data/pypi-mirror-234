import os
from dig_git_ignore import main
from dig_git_ignore import constants

# pylint: disable=protected-access,no-member


def test_create_without_existing_gitignore() -> None:
    os.remove(constants.GITIGNORE_FILENAME)
    main._main(["create", "python"])


def test_create_with_existing_gitignore() -> None:
    with open(constants.GITIGNORE_FILENAME, mode="wt", encoding="utf-8") as file:
        file.write("# Non empty file")
    main._main(["create", "python"])
