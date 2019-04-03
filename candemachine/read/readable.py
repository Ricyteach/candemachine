from ..exceptions import CandeFormatError


class CandeReadableMixin:
    _from_dict = dict(cid="from_cid")  # methods to build instance from given format

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(cls, **kwargs)
        if not all(hasattr(cls, attr) for attr in cls._from_dict.values()):
            raise CandeFormatError(f'{cls.__qualname__!r} class missing method(s): '
                                   f'{", ".join(attr for attr in cls._from_dict.values())}')
