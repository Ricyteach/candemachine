import abc
import enum
import logging
from dataclasses import dataclass, field
from pathlib import Path
from typing import List

from candemachine.serialize import serialize
from candemachine.deserialize import deserialize
from .formats import CandeFormattableMixin
from .exceptions import CandeReadError
from .pipe_groups import PipeGroup
from .materials import Material
from .utilities import mutate_barray_for_preamble, mod_str_to_bytearray, ValuesGenMixin


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


@dataclass(eq=False)
class CandeBase(CandeFormattableMixin, abc.ABC):
    """Base class for CandeL1, CandeL2, and CandeL3 problems"""
    method:Method
    mode: Mode
    level: Level = Level.THREE
    heading: str = "From `candemachine` by: Rick Teachey, rick@teachey.org"
    iterations: int = field(default=-99, init=False, repr=False)

    # children
    pipe_groups: List[PipeGroup] = field(default_factory=list, init=False, repr=False)
    materials: List[Material] = field(default_factory=list, init=False, repr=False)

    def __post_init__(self):
        self.method = Method(self.method)
        self.mode = Mode(self.mode)
        self.level = Level(self.level)
        if len(self.heading)>60:
            logging.debug(f"Truncated heading {len(self.heading)-60} characters")
            self.heading = self.heading[:60]

    def cid_format(self):
        result_strs = []
        result_strs.append(f'{self.mode.value: <8}{self.level.value: >2d}{self.method.value: >2d}{self.n_pipe_groups: >3d}{self.heading: <60}{self.iterations: >5d}')
        return ''.join(result_strs)

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
            mode = Mode(line[:8].decode().strip()),
            level = Level(int(line[8:10])),
            method = Method(int(line[10:12])),
            heading = line[15:75].decode(),
        )
        obj.n_pipe_groups = int(line[12:15]),
        del line[:75]
        return obj

    @property
    def n_pipe_groups(self):
        return len(self.pipe_groups)

    @n_pipe_groups.setter
    def n_pipe_groups(self, n):
        # TODO: figure this, uh, out.
        self._n_pipe_groups = n

    def write(self, p: Path, output="cid", mode="x"):
        with p.open(mode=mode) as fout:
            fout.write("\n".join(serialize(output)))

    @classmethod
    def read(cls, p: Path):
        if p.suffix != "cid":
            raise CandeReadError(f"File type {p.suffix!r} not supported.")
        with p.open(mode="r") as fin:
            return deserialize(fin, p.suffix)

    def __iter__(self):
        yield from (self.pipe_groups, *self.problem_contents, self.materials)

    @property
    @abc.abstractmethod
    def problem_contents(self):
        """An iterable of all the information specific to the Cande problem level.

        Example: Level3 ASD will produce C1, C2, C3, C4, and C5 info
        """
        ...
