from candemachine.exceptions import CandeDeserializationError


# TODO: implement this thing
def deserialize(cls, lines, input="cid"):
    if input != "cid":
        raise CandeDeserializationError(f"Input type {input!r} not supported.")
    ilines = iter(lines)
    obj = cls.from_cid(next(ilines))
    for child in obj.ichildren():
        child.deserialize(ilines)
    return obj