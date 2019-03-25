import pytest

from candemachine.utilities import mod_args, Decimal


@pytest.fixture
def is_str():
    """An str type check modded to also pass for ints"""
    @mod_args(test_func=lambda arg: isinstance(arg, int), mod_func=lambda arg: str(arg))
    def func(some_int):
        return isinstance(some_int, str)
    return func


def test_mod_args_int(is_str):
    assert is_str(123456)


def test_mod_args_str(is_str):
    assert is_str("string")


def test_mod_args_not_int(is_str):
    assert not is_str(1.1)
    assert not is_str([])


class TestDecimal:
    def test_new_new(self):
        assert Decimal(bytearray(' -1.34 '.encode()))