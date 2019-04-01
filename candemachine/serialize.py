from typing import Iterable

from candemachine.formats import CandeFormattableMixin
from .exceptions import CandeDeserializationError, CandeSerializationError


# TODO: implement this thing
def deserialize(cls, lines, input="cid"):
    if input != "cid":
        raise CandeDeserializationError(f"Input type {input!r} not supported.")
    ilines = iter(lines)
    obj = cls.from_cid(next(ilines))
    for child in obj.ichildren():
        child.deserialize(ilines)
    return obj


def serialize(obj, output="cid"):
    try:
        yield f"{obj:{output}}"
    except ValueError as e:
        raise CandeSerializationError(f"Output type {output!r} not supported.") from e
    if isinstance(obj, Iterable):
        for item in obj:
            yield from serialize(item, output)
