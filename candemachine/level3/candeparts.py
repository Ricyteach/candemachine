from __future__ import annotations
from dataclasses import dataclass, field
from typing import Optional

from ..formats import CandeFormattableMixin
from ..exceptions import CandeFormatError
from ..utilities import Decimal, mutate_barray_for_preamble, mod_str_to_bytearray


@dataclass
class CandePart(CandeFormattableMixin):
    last: bool = field(default=False, init=False, repr=False)
    num: int = 0

    @staticmethod
    @mod_str_to_bytearray
    def remove_preamble(line):
        # break off preamble line if it is there
        mutate_barray_for_preamble(line, test_func=lambda x: not x[1:5].decode().strip().isdigit())

    @classmethod
    @mod_str_to_bytearray
    def from_cid(cls, line):
        cls.remove_preamble(line)
        num = int(line[1:5])
        obj = cls(num)
        obj.last = line[0]=="L"
        del line[:5]
        return obj

    def __format__(self, format_spec):
        if format_spec != 'cid':
            raise CandeFormatError(f'Invalid format_spec: {format_spec!r}')
        return f'{"L" if self.last else " "}{self.num: >4d}'


@dataclass
class Node(CandePart):
    x: Decimal = Decimal()
    y: Decimal = Decimal()
    master: Optional[Node] = None

    @classmethod
    @mod_str_to_bytearray
    def from_cid(cls, line):
        obj = super().from_cid(line)
        obj.x, obj.y = Decimal(line[5:15]), Decimal(line[15:25])
        del line[:25]
        return obj

    def __format__(self, format_spec):
        results_strs = [super().__format__(format_spec)]
        results_strs.append(f'     {self.x: >10G}{self.y: >10G}')
        return ''.join(results_strs)


@dataclass
class Element(CandePart):
    i: int = 0
    j: int = 0
    k: int = 0
    l: int = 0
    mat: int = 0
    step: int = 0
    type: int = 0
    death: int = 0

    @classmethod
    @mod_str_to_bytearray
    def from_cid(cls, line):
        obj = super().from_cid(line)
        obj.i, obj.j, obj.k, obj.l, obj.mat, obj.step = int(line[1:5]), int(line[5:10]), int(line[10:15]), int(line[15:20]), int(line[20:25]), int(line[25:30])
        if line[30:35].strip():
            obj.type = int(line[30:35])
        if line[50:55].strip():
            obj.type = int(line[50:55])
        del line[:55]
        return obj

    def __format__(self, format_spec):
        result_strs = [super().__format__(format_spec)]
        result_strs.append(f'{self.i: >5d}{self.j: >5d}{self.k: >5d}{self.l: >5d}{self.mat: >5d}{self.step: >5d}')
        result_strs.append('' if self.type==0 else f'{self.type: >5d}')
        result_strs.append('' if self.death==0 else f'{"": <15}{self.death: >5d}')
        return ''.join(result_strs)


@dataclass
class Boundary(CandePart):
    node: int = 0
    xcode: int = 0
    xvalue: Decimal = Decimal()
    ycode: int = 0
    yvalue: Decimal = Decimal()
    angle: Decimal = Decimal()
    step: int = 0

    @classmethod
    @mod_str_to_bytearray
    def from_cid(cls, line, num=0):
        cls.remove_preamble(line)
        obj = cls(num)
        obj.node, obj.xcode, obj.xvalue, obj.ycode, obj.yvalue, obj.angle, obj.step = int(line[1:5]), int(line[5:10]), Decimal(line[10:20]), int(line[20:25]), Decimal(line[25:35]), Decimal(line[35:45]), int(line[45:50])
        del line[:50]
        return obj

    def __format__(self, format_spec):
        result_strs = [super().__format__(format_spec)[:1]]
        result_strs.append(f'{self.node: >4d}{self.xcode: >5d}{self.xvalue: >10G}{self.ycode: >5d}{self.yvalue: >10G}'
                           f'{self.angle: >10G}{self.step: >5d}')
        return ''.join(result_strs)
