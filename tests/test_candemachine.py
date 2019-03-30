import pytest
import candemachine
from candemachine.candemain import CandeBase, Mode
from candemachine.exceptions import CandeSerializationError


class TestCandeBase:
    @pytest.fixture
    def BasicCande(self):
        class BasicCande(CandeBase):
            @property
            def problem_contents(self):
                return []
        return BasicCande

    @pytest.fixture
    def asd_anal_l3_cande(self, BasicCande):
        return BasicCande(0, Mode.ANALYSIS, level=3)

    @pytest.fixture
    def cid(self):
        return "ANALYS   3 0  0From `candemachine` by: Rick Teachey, rick@teachey.org        -99"

    def test_init(self, asd_anal_l3_cande):
        assert asd_anal_l3_cande

    def test_iter(self, asd_anal_l3_cande):
        asd_anal_l3_cande.materials = [1]
        assert list(iter(asd_anal_l3_cande)) == [asd_anal_l3_cande, 1]

    def test_cid_format(self, asd_anal_l3_cande, cid):
        assert f"{asd_anal_l3_cande:cid}" == cid

    def test_from_cid(self, BasicCande, cid):
        assert BasicCande.from_cid(cid)

    def test_serialize(self, asd_anal_l3_cande):
        with pytest.raises(CandeSerializationError):
            next(asd_anal_l3_cande.serialize(output="foo"))
        next(asd_anal_l3_cande.serialize(output="cid"))
        next(asd_anal_l3_cande.serialize(output="cid"))  # already tested in cid_format
        next(asd_anal_l3_cande.serialize(output="cid"))  # already tested in cid_format
        next(asd_anal_l3_cande.serialize(output="cid"))  # already tested in cid_format
        assert next(asd_anal_l3_cande.serialize(output="cid")) == ""

class TestNode:
    @pytest.fixture
    def cidL(self):
        return "L   1       1.0       1.0"

    @pytest.fixture
    def info(self):
        return dict(num=1, x=1.0, y=1.0)

    @pytest.fixture
    def node(self, info):
        return candemachine.Node(**info)

    def test_attrs(self, node, info):
        assert (node.num, node.x, node.y) == (*info.values(),)

    def test_cid_format(self, node, info):
        result = f'   {info["num"]}     {info["x"]: >10G}{info["y"]: >10G}'
        assert format(node, 'cid') == ' ' + result
        node.last = True
        assert format(node, 'cid') == 'L' + result

    def test_from_cid(self, cidL):
        assert candemachine.Node.from_cid(cidL)


class TestElement:
    @pytest.fixture
    def cidL(self):
        return "L   1    1    2    3    4    1    1    8    3"

    @pytest.fixture
    def info(self):
        return dict(num=1, i=1, j=2, k=3, l=4, mat=1, step=1, type=8, death=3)

    @pytest.fixture
    def element(self, info):
        return candemachine.Element(**info)

    def test_attrs(self, element, info):
        assert (element.num, element.i, element.j, element.k, element.l,
                element.mat, element.step, element.type, element.death) == (*info.values(),)

    def test_cid_format(self, element, info):
        result = f'   {info["num"]}{info["i"]: >5d}{info["j"]: >5d}{info["k"]: >5d}{info["l"]: >5d}{info["mat"]: >5d}{info["step"]: >5d}'
        result += '' if element.type==0 else f'{element.type: >5d}'
        result += '' if element.death==0 else f'               {element.death: >5d}'
        assert format(element, 'cid') == ' ' + result
        element.last = True
        assert format(element, 'cid') == 'L' + result

    def test_from_cid(self, cidL):
        assert candemachine.Element.from_cid(cidL)


class TestBoundary:
    @pytest.fixture
    def cidL(self):
        return "L  25    1        10    1        10         0    1"

    @pytest.fixture
    def info(self):
        return dict(num=1, node=25, xcode=1, xvalue=10, ycode=1, yvalue=10, angle=0, step=1)

    @pytest.fixture
    def boundary(self, info):
        return candemachine.Boundary(**info)

    def test_attrs(self, boundary, info):
        assert (boundary.num, boundary.node, boundary.xcode, boundary.xvalue, boundary.ycode, boundary.yvalue,
                boundary.angle, boundary.step) == (*info.values(),)

    def test_cid_format(self, boundary, info):
        result = f'  {info["node"]}{info["xcode"]: >5d}{info["xvalue"]: >10G}{info["ycode"]: >5d}{info["yvalue"]: >10G}' \
            f'{info["angle"]: >10G}{info["step"]: >5d}'
        assert format(boundary, 'cid') == ' ' + result
        boundary.last = True
        assert format(boundary, 'cid') == 'L' + result

    def test_from_cid(self, cidL):
        assert candemachine.Boundary.from_cid(cidL)
