from abc import ABC

from candemachine.exceptions import CandeFormatError


class CandeFormattableMixin:
    _spec_dict = dict(cid="cid_format")

    def __format__(self, format_spec):
        try:
            formatter = self._spec_dict[format_spec]
        except KeyError as e:
            raise CandeFormatError(f'Invalid format_spec: {format_spec!r}') from e
        try:
            return getattr(self, formatter)()
        except AttributeError as e:
            raise CandeFormatError(f'{formatter!r} method not implemented') from e
