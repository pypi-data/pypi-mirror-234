from dig_git_ignore import main

# pylint: disable=protected-access,no-member


def test_list_all() -> None:
    main._main(["list-all"])
