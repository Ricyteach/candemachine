class CandeError(Exception):
    pass


class CandeSerializationError(CandeError):
    pass


class CandeDeserializationError(CandeError):
    pass


class CandeReadError(CandeError):
    pass


class CandePartError(CandeError):
    pass


class CandeFormatError(CandePartError):
    pass
