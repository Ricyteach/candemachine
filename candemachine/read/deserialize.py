from ..exceptions import CandeDeserializationError
from . import cid as cid_read
from . import msh as msh_read

DESERIALIZERS = dict(cid=cid_read,
                     msh=msh_read,
                     )


# TODO: implement this thing
def deserialize(pieces, input="cid"):
    ipieces = iter(pieces)
    try:
        deserializer_module = DESERIALIZERS[input]
    except KeyError as e:
        raise CandeDeserializationError(f"Input type {input!r} not yet supported.") from e
    try:
        deserializer = deserializer_module.process
    except AttributeError as e:
        raise CandeDeserializationError("Deserializer is missing the process() method.") from e
    obj = deserializer(ipieces)
    return obj
