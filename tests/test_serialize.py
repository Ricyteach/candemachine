from candemachine.serialize import serialize, deserialize


class TestDeserialize:
    pass


class TestSerialize:
    def test_serialize_atomic(self):
        assert list(serialize(1, output="d")) == ["1"]
