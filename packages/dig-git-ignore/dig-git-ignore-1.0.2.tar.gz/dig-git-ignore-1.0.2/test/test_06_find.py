from dig_git_ignore import main

# pylint: disable=protected-access,no-member


def test_find_existing_py() -> None:
    main._main(["find", "py"])


def test_find_existing_python() -> None:
    main._main(["find", "python"])


def test_find_not_exists() -> None:
    main._main(["find", "f66e8da2-ef7b-45a4-9410-dd9a5ddc4052"])
