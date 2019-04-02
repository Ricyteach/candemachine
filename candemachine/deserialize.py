from candemachine.exceptions import CandeDeserializationError


# TODO: implement this thing
def deserialize(cls_or_obj, lines, input="cid", parent=None):
    ilines = iter(lines)
    try:
        deserializer = cls_or_obj._from_dict[input]
    except KeyError as e:
        raise CandeDeserializationError(f"Input type {input!r} not supported.") from e
    except AttributeError as e:
        obj = deserializer(next(ilines))
        for child in obj:
            child.deserialize(ilines)
        return obj
