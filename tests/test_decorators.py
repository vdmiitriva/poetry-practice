import pytest

from src.decorators import log


@log()
def add(a: int, b: int) -> int:
    return a + b


def test_add(capsys):
    result = add(2, 3)
    captured = capsys.readouterr()

    assert result == 5
    assert captured.out == "add ok\n"


@log()
def divide(a: int, b: int) -> float:
    return a / b


def test_divide_error(capsys):
    with pytest.raises(ZeroDivisionError):
        divide(10, 0)

    captured = capsys.readouterr()

    assert captured.out == ("divide error: division by zero. Inputs: (10, 0), {}\n")


def test_multiply_to_file(tmp_path):
    log_file = tmp_path / "log.txt"

    @log(str(log_file))
    def multiply(a, b):
        return a * b

    result = multiply(2, 3)

    assert result == 6
    assert log_file.read_text() == "multiply ok\n"


def test_divide_error_to_file(tmp_path):
    log_file = tmp_path / "log.txt"

    @log(str(log_file))
    def divide(a, b):
        return a / b

    with pytest.raises(ZeroDivisionError):
        divide(10, 0)

    assert log_file.read_text() == ("divide error: division by zero. Inputs: (10, 0), {}\n")
