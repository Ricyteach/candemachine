import pytest

from candemachine.exceptions import CandeSerializationError
from candemachine.serialize import serialize
from candemachine.deserialize import deserialize


class TestDeserialize:
    minimal_cid = "ANALYS   3 1  3Box 28N 6.4ft Cover 0.125Gage HS-20                           -99",

    def test_minimal_cid(self):
        cande_obj_minimal = deserialize(self.minimal_cid)
        assert cande_obj_minimal

    l3_cid = """
    PREP BRIDGECOR
       22    3    0    3    1 1204 1167   99    4   37    1
        1    0    98.503     0.000
        2    0    97.733     6.572
    L   3    0    96.963    13.145
    L   1    1    2    3    0    1    1    0
    L   1    1     0.000    0     0.000     0.000    1    0    0     0.000     0.000
    """[1:-1].split("\n")

    def test_l3_cid(self):
        L3_obj = deserialize(self.l3_cid)
        assert L3_obj

    node_cid = "L   3    0    96.963    13.145",

    def test_node_cid(self):
        node_obj = deserialize(self.node_cid)
        assert node_obj


class TestSerialize:
    def test_serialize_atomic(self):
        assert list(serialize(1, output="d")) == ["1"]

    def test_serialize_iterable_non_str(self):
        assert list(serialize([1], output="d")) == ["1"]

    def test_serialize_str(self):
        assert list(serialize("string", output="")) == ["string"]

    def test_serialize_failure(self):
        with pytest.raises(CandeSerializationError):
            list(serialize(1))  # output="cid" (default)
