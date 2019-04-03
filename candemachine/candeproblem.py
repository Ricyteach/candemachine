import abc
import logging
from dataclasses import dataclass, field, InitVar
from pathlib import Path
from typing import List

from .candemain import Mode, Method, Level, CandeMain
from candemachine.write.serialize import serialize
from .read.deserialize import deserialize
from candemachine.write.formattable import CandeFormattableMixin
from candemachine.read.readable import CandeReadableMixin
from .exceptions import CandeReadError
from .pipe_groups import PipeGroup
from .materials import Material


@dataclass(eq=False)
class CandeProbBase(CandeFormattableMixin, CandeReadableMixin, abc.ABC):
    """Base class for CandeL1, CandeL2, and CandeL3 problems"""
    method_: InitVar[Method]
    mode_: InitVar[Mode]
    level_: InitVar[Level] = Level.THREE
    heading_: str = "From `candemachine` by: Rick Teachey, rick@teachey.org"
    iterations_: int = field(default=-99, init=False, repr=False)

    # children
    pipe_groups: List[PipeGroup] = field(default_factory=list, init=False, repr=False)
    materials: List[Material] = field(default_factory=list, init=False, repr=False)

    def __post_init__(self, method_, mode_, level_):
        self._cande = CandeMain(Method(method_), Mode(mode_), Level(level_))
        self.truncate_heading()

    @property
    def method(self):
        return self._cande.method

    @property
    def mode(self):
        return self._cande.mode

    @property
    def level(self):
        return self._cande.level

    @property
    def heading(self):
        return self._cande.heading

    @property
    def iterations(self):
        return self._cande.iterations

    def cid_format(self):
        result_strs = []
        result_strs.append(f'{self.mode.value: <8}{self.level.value: >2d}{self.method.value: >2d}{self.n_pipe_groups: >3d}{self.heading: <60}{self.iterations: >5d}')
        return ''.join(result_strs)

    @property
    def n_pipe_groups(self):
        return len(self.pipe_groups)

    def write(self, p: Path, output="cid", mode="x"):
        with p.open(mode=mode) as fout:
            fout.write("\n".join(serialize(output)))

    @classmethod
    def from_candemain(cls, main):
        if main.heading is None:
            main.heading = cls.__dataclass_fields__["heading_"].default
        if main.iterations is None:
            main.iterations = cls.__dataclass_fields__["iterations_"].default
        obj = cls.__new__(cls)
        obj._cande = main
        obj.truncate_heading()
        return obj

    def truncate_heading(self):
        if len(self.heading)>60:
            logging.debug(f"Truncated heading {len(self._cande.heading)-60} characters")
            self._cande.heading = self._cande.heading[:60]

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
