from __future__ import annotations
from dataclasses import dataclass
from decimal import Decimal
from typing import Optional


class CandePartError(Exception):
    pass


class CandeFormatError(CandePartError):
    pass


@dataclass
class CandePart:
    num: int = 0

    def __format__(self, format_spec):
        if format_spec == 'cid':
            return f'{self.num: >5d}'
        if format_spec == 'cidL':
            return f'L{self.num: >4d}'
        raise CandeFormatError(f'Invalid format_spec: {format_spec!r}')


@dataclass
class Node(CandePart):
    x: Decimal = Decimal()
    y: Decimal = Decimal()
    master: Optional[Node] = None

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

    def __format__(self, format_spec):
        result_strs = [super().__format__(format_spec)[0]]
        result_strs.append(f'{self.node: >4d}{self.xcode: >5d}{self.xvalue: >10G}{self.ycode: >5d}{self.yvalue: >10G}'
                           f'{self.angle: >10G}{self.step: >5d}')
        return ''.join(result_strs)
