import os

import pytest

from src.decorators import log


def test_log(capsys):
    @log()
    def add(a, b):
        return a + b

    add(2, 3)
    captured = capsys.readouterr()
    assert captured.out == "add ok: 5\n\n"


def test_log_error(capsys):
    @log()
    def faulty_func():
        raise TypeError("test error")

    with pytest.raises(TypeError):
        faulty_func()

    captured = capsys.readouterr()
    assert captured.out == "faulty_func TypeError: test error. Inputs: (), {}\n\n"


def test_log_to_file():
    @log("test.log")
    def add_str(a, b="7"):
        return a + b

    if os.path.exists("logs/test.log"):
        os.remove("logs/test.log")

    add_str("2", b="10")

    assert os.path.exists("logs/test.log")

    with open("logs/test.log", "r") as f:
        text_log = f.read()
        assert text_log == "add_str ok: 210\n"


def test_error_log_to_file():
    @log("test_2.log")
    def faulty_func():
        raise ValueError("test error")

    if os.path.exists("logs/test_2.log"):
        os.remove("logs/test_2.log")

    with pytest.raises(ValueError):
        faulty_func()

    assert os.path.exists("logs/test_2.log")

    with open("logs/test_2.log", "r") as f:
        text_log = f.read()
        assert text_log == "faulty_func ValueError: test error. Inputs: (), {}\n"
