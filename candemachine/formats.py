from abc import ABC

from candemachine.exceptions import CandeFormatError


class CandeFormattableMixin:
    _spec_dict = dict(cid="cid_format")  # methods to format to given format key
    _from_dict = dict(cid="from_cid")  # methods to build instance from given format

    def __init_subclass__(cls, **kwargs):
        if not all(hasattr(cls, attr) for d in (cls._spec_dict, cls._from_dict) for attr in d.values()):
            raise CandeFormatError(f'{cls.__qualname__!r} class missing method(s): '
                                   f'{"".join(attr for d in (cls._spec_dict, cls._from_dict) for attr in d)}')

    def __format__(self, format_spec):
        try:
            formatter = self._spec_dict[format_spec]
        except KeyError as e:
            raise CandeFormatError(f'Invalid format_spec: {format_spec!r}') from e
        try:
            return getattr(self, formatter)()
        except AttributeError as e:
            raise CandeFormatError(f'{formatter!r} method not implemented') from e
