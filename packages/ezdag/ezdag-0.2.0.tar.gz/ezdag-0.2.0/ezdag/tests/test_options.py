import os.path

import pytest

from ..options import Argument, Option


@pytest.mark.parametrize(
    "name,value,is_file",
    [
        ["index", 1, False],
        ["format", "csv", False],
        ["input", "file1.txt", True],
        ["input", "path/to/file1.txt", True],
    ],
)
def test_argument_commands_single(name, value, is_file):
    argument = Argument(name, value)

    assert argument.name == name
    assert argument.vars() == str(value)

    if is_file:
        assert argument.files() == value

        filename = os.path.basename(value)
        assert argument.files(basename=True) == filename

        if filename == value:
            assert not argument.remaps()
        else:
            assert argument.remaps() == f"{filename}={value}"


def test_option_commands_flag():
    name = "verbose"
    option = Option(name)

    assert option.name == name
    assert option.vars() == f"--{name}"


@pytest.mark.parametrize(
    "name,value,is_file",
    [
        ["index", 1, False],
        ["format", "csv", False],
        ["input", "file1.txt", True],
        ["input", "path/to/file1.txt", True],
    ],
)
def test_option_commands_single(name, value, is_file):
    option = Option(name, value)

    assert option.name == name
    assert option.vars() == f"--{name} {value}"

    if is_file:
        assert option.files() == value

        filename = os.path.basename(value)
        assert option.files(basename=True) == filename

        if filename == value:
            assert not option.remaps()
        else:
            assert option.remaps() == f"{filename}={value}"
