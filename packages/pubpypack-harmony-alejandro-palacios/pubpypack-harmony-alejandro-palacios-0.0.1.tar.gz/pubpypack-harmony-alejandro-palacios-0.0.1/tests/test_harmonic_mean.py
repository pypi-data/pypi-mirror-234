import sys

import pytest
from termcolor import colored

from imppkg.harmony import main


@pytest.mark.parametrize(
    "inputs, expected",
    [
        (["3", "3", "3"], 3.0),
        ([], 0.0),
        (["foo", "bar"], 0.0),
    ],
)
def test_harmony_parametrized(inputs, monkeypatch, capsys, expected):
    monkeypatch.setattr(sys, "argv", ["harmony"] + inputs)
    main()
    expected = colored(expected, "red", "on_cyan", attrs=["bold"])
    assert capsys.readouterr().out.strip() == expected


FRUITS = ["apple"]


def test_len():
    assert len(FRUITS) == 1
