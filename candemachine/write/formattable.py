from ..exceptions import CandeFormatError


class CandeFormattableMixin:
    _spec_dict = dict(cid="cid_format")  # methods to format to given format key

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(cls, **kwargs)
        if not all(hasattr(cls, attr) for attr in cls._spec_dict.values()):
            raise CandeFormatError(f'{cls.__qualname__!r} class missing method(s): '
                                   f'{", ".join(attr for attr in cls._spec_dict.values())}')

    def __format__(self, format_spec):
        try:
            formatter = self._spec_dict[format_spec]
        except KeyError as e:
            raise CandeFormatError(f'Invalid format_spec: {format_spec!r}') from e
        try:
            return getattr(self, formatter)()
        except AttributeError as e:
            raise CandeFormatError(f'{formatter!r} method not implemented') from e
