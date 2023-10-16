import os
from dig_git_ignore import main
from dig_git_ignore import constants

# pylint: disable=protected-access,no-member


def test_update_without_existing_gitignore() -> None:
    os.remove(constants.GITIGNORE_FILENAME)
    main._main(["update"])


def test_update_with_existing_gitignore_without_existing_template() -> None:
    with open(constants.GITIGNORE_FILENAME, mode="wt", encoding="utf-8") as file:
        file.write("# Non empty file")
    main._main(["update"])


def test_update_with_existing_gitignore_with_existing_template() -> None:
    main._main(["create", "python"])
    main._main(["update"])
