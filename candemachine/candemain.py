import enum
from dataclasses import dataclass, field
from typing import Optional

from .utilities import ValuesGenMixin, mod_str_to_bytearray, mutate_barray_for_preamble


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

    @staticmethod
    @mod_str_to_bytearray
    def remove_preamble(line):
        # break off preamble line if it is there
        mutate_barray_for_preamble(line, test_func=lambda x: not x[:8].decode().strip() in Mode.values_gen())

    @classmethod
    @mod_str_to_bytearray
    def from_cid(cls, line):
        cls.remove_preamble(line)
        obj = cls(
            mode=Mode(line[:8].decode().strip()),
            level=Level(int(line[8:10])),
            method=Method(int(line[10:12])),
            n_pipe_groups=int(line[12:15]),
            heading=line[15:75].decode(),
            iterations=int(line[75:80]),
        )
        del line[:80]
        return obj
