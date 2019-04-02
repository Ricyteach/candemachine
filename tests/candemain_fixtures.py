import pytest
from candemachine.candeproblem import CandeProbBase
from candemachine.candemain import Mode


@pytest.fixture
def BasicCande():
    class BasicCande(CandeProbBase):
        @property
        def problem_contents(self):
            return []
    return BasicCande


@pytest.fixture
def basic_cande_asd_anal_L3(BasicCande):
    return BasicCande(0, Mode.ANALYSIS, level=3)


@pytest.fixture
def basic_cande_asd_anal_L3_cid():
    return "ANALYS   3 0  0From `candemachine` by: Rick Teachey, rick@teachey.org        -99"
