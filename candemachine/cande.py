import itertools

from .candemain import Mode, Method, Level, CandeMain
from .candetypes import CandeL1AnalysisASD, CandeL2AnalysisASD, CandeL3AnalysisASD, CandeL1DesignASD, CandeL2DesignASD,\
    CandeL3DesignASD, CandeL1AnalysisLRFD, CandeL2AnalysisLRFD, CandeL3AnalysisLRFD, CandeL1DesignLRFD,\
    CandeL2DesignLRFD, CandeL3DesignLRFD

CANDE_CLS_KEYS = tuple(CandeMain(Method(method), Mode(mode), Level(level))
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


def cande(method, mode, level=3, heading=None, iterations=None, n_pipe_groups=None):
    """Factory for creating Cande problem instances."""
    # alternative names for designating the method
    mode = {"ANALYSIS": "ANALYS", 0: "ANALYS", 1: "DESIGN", "A": "ANALYS", "D": "DESIGN"}.get(mode, mode)
    cande_main = CandeMain(method=Method(method), mode=Mode(mode), level=Level(level), heading=heading,
                           iterations=iterations, n_pipe_groups=n_pipe_groups)
    cls = CANDE_CLS_DICT[cande_main]
    return cls.from_candemain(cande_main)
