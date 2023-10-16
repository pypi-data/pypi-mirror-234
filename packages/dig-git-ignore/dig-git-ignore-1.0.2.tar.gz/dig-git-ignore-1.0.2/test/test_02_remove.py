import os
from dig_git_ignore import main
from dig_git_ignore import constants

# pylint: disable=protected-access,no-member


def test_remove_without_existing_gitignore() -> None:
    os.remove(constants.GITIGNORE_FILENAME)
    main._main(["remove", "python"])


def test_remove_with_existing_gitignore_without_existing_template() -> None:
    with open(constants.GITIGNORE_FILENAME, mode="wt", encoding="utf-8") as file:
        file.write("# Non empty file")
    main._main(["remove", "python"])


def test_remove_with_existing_gitignore_with_existing_template_has_to_exclude() -> None:
    main._main(["create", "python", "c++"])
    main._main(["remove", "c++"])


def test_remove_with_existing_gitignore_with_existing_template_do_not_has_to_exclude() -> None:
    main._main(["create", "python"])
    main._main(["remove", "c++"])


def test_remove_with_existing_gitignore_with_existing_template_last_template() -> None:
    main._main(["create", "python"])
    main._main(["remove", "python"])
