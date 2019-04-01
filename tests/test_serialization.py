import pytest

from candemachine.exceptions import CandeSerializationError
from candemachine.serialize import serialize
from candemachine.deserialize import deserialize


class TestDeserialize:
    pass


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
