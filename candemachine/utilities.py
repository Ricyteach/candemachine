import enum
from functools import  wraps
import decimal


def mod_args(test_func, mod_func):
    """A decorator that modifies arguments when the test_func returns true for the argument."""
    def wrapper(func):
        @wraps(func)
        def wrapped(*args, **kwargs):
            args = [mod_func(arg) if test_func(arg) else arg for arg in args]
            kwargs = {k:mod_func(v) if test_func(v) else v for k,v in kwargs.items()}
            return func(*args, **kwargs)
        return wrapped
    return wrapper


class ValuesGenMixin:
    """Extends enums with a generator of all the values"""
    @classmethod
    def values_gen(cls):
        return (v.value for v in list(cls))


class Decimal(decimal.Decimal):

    @classmethod
    def from_bytearray(cls, barray, context=None):
        if context:
            return cls(barray.decode(), context)
        return cls(barray.decode())

    @wraps(decimal.Decimal.__new__)
    def __new__(cls, value="0", context=None):
        try:
            return super().__new__(cls, value, context)
        except TypeError as e:
            if isinstance(value, bytearray):
                return cls.from_bytearray(value, context)
            raise e


def mutate_barray_for_preamble(line, *, test_func):
    """Gets rid of the CANDE preamble line that is optional in input files"""
    assert isinstance(line, bytearray)
    if test_func(line):
        del line[:27]


mod_str_to_bytearray = mod_args(test_func=lambda arg: isinstance(arg, str), mod_func=lambda arg: bytearray(arg.encode()))