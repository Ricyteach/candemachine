import pytest
import candemachine


# candeparts.Node
@pytest.fixture
def node_cidL():
    return "L   1       1.0       1.0"


@pytest.fixture
def node_info():
    return dict(num=1, x=1.0, y=1.0)


@pytest.fixture
def node(node_info):
    return candemachine.Node(**node_info)


# candeparts.Element
@pytest.fixture
def element_cidL():
    return "L   1    1    2    3    4    1    1    8    3"


@pytest.fixture
def element_info():
    return dict(num=1, i=1, j=2, k=3, l=4, mat=1, step=1, type=8, death=3)


@pytest.fixture
def element(element_info):
    return candemachine.Element(**element_info)


# candeparts.Boundary
@pytest.fixture
def boundary_cidL():
    return "L  25    1        10    1        10         0    1"


@pytest.fixture
def boundary_info():
    return dict(num=1, node=25, xcode=1, xvalue=10, ycode=1, yvalue=10, angle=0, step=1)


@pytest.fixture
def boundary(boundary_info):
    return candemachine.Boundary(**boundary_info)
