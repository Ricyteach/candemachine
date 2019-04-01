from typing import Iterable
from .exceptions import CandeSerializationError


def serialize(obj, output="cid"):
    try:
        yield f"{obj:{output}}"
    except Exception as e:
        if isinstance(obj, Iterable) and not isinstance(obj, str):
            for item in obj:
                yield from serialize(item, output)
        else:
            raise CandeSerializationError(f"Output type {output!r} not supported.") from e
