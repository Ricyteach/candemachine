import enum
from dataclasses import dataclass, field
from typing import Optional

from .exceptions import CandeDeserializationError
from .utilities import ValuesGenMixin


class Mode(ValuesGenMixin, enum.Enum):
    ANALYSIS = "ANALYS"
    DESIGN = "DESIGN"
    STOP = "STOP"


class Method(ValuesGenMixin, enum.IntEnum):
    SERVICE = 0
    FACTORED = 1
    ASD = 0
    LRFD = 1


class Level(ValuesGenMixin, enum.IntEnum):
    BASIC = 1
    CANNED = 2
    USER = 3
    ONE = 1
    TWO = 2
    THREE = 3


@dataclass
class CandeMain:
    method: Method
    mode: Mode
    level: Level
    n_pipe_groups: Optional[int] = field(compare=False, default=None)
    heading: Optional[str] = field(compare=False, default=None)
    iterations: Optional[int] = field(compare=False, default=None)

    @classmethod
    def from_cid(cls, line):
        try:
            obj = cls(
                mode=Mode(line[:8].decode().strip()),
                level=Level(int(line[8:10])),
                method=Method(int(line[10:12])),
                n_pipe_groups=int(line[12:15]),
                heading=line[15:75].decode(),
                iterations=int(line[75:80]),
            )
        except Exception as e:
            raise CandeDeserializationError(f"Failed to read line:\b{line!r}") from e
        else:
            return obj
