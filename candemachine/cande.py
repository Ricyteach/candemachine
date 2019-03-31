import itertools
from typing import NamedTuple

from .candemain import Method, Mode, Level
from .candetypes import CandeL1AnalysisASD, CandeL2AnalysisASD, CandeL3AnalysisASD, CandeL1DesignASD, CandeL2DesignASD,\
    CandeL3DesignASD, CandeL1AnalysisLRFD, CandeL2AnalysisLRFD, CandeL3AnalysisLRFD, CandeL1DesignLRFD,\
    CandeL2DesignLRFD, CandeL3DesignLRFD


class CandeCls(NamedTuple):
    method: Method
    mode: Mode
    level: Level


CANDE_CLS_KEYS = tuple(CandeCls(Method(method), Mode(mode), Level(level))
                       for method, mode, level
                       in itertools.product(range(2), ("ANALYS", "DESIGN"), range(1,4))
                       )

CANDE_OPTIONS = (
    CandeL1AnalysisASD, CandeL2AnalysisASD, CandeL3AnalysisASD,
    CandeL1DesignASD, CandeL2DesignASD, CandeL3DesignASD,
    CandeL1AnalysisLRFD, CandeL2AnalysisLRFD, CandeL3AnalysisLRFD,
    CandeL1DesignLRFD, CandeL2DesignLRFD, CandeL3DesignLRFD,
)

CANDE_CLS_DICT = dict(zip(CANDE_CLS_KEYS, CANDE_OPTIONS))


def cande(method, mode, level=3, heading=None):
    """Factory for creating Cande problem instances."""
    # alternative names for designating the method
    mode = {"ANALYSIS": "ANALYS", 0: "ANALYS", 1: "DESIGN", "A": "ANALYS", "D": "DESIGN"}.get(mode, mode)
    key = CandeCls(Method(method), Mode(mode), Level(level))
    return CANDE_CLS_DICT[key]
