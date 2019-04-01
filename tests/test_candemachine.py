import candemachine


class TestCandeBase:
    def test_init(self, basic_cande_asd_anal_L3):
        assert basic_cande_asd_anal_L3

    def test_iter(self, basic_cande_asd_anal_L3):
        basic_cande_asd_anal_L3.materials = [1]
        assert list(iter(basic_cande_asd_anal_L3)) == [[], [1]]


class TestNode:
    def test_attrs(self, node, node_info):
        assert (node.num, node.x, node.y) == (*node_info.values(),)

    def test_from_cid(self, node_cidL):
        assert candemachine.Node.from_cid(node_cidL)


class TestElement:
    def test_attrs(self, element, element_info):
        assert (element.num, element.i, element.j, element.k, element.l,
                element.mat, element.step, element.type, element.death) == (*element_info.values(),)

    def test_from_cid(self, element_cidL):
        assert candemachine.Element.from_cid(element_cidL)


class TestBoundary:
    def test_attrs(self, boundary, boundary_info):
        assert (boundary.num, boundary.node, boundary.xcode, boundary.xvalue, boundary.ycode, boundary.yvalue,
                boundary.angle, boundary.step) == (*boundary_info.values(),)

    def test_from_cid(self, boundary_cidL):
        assert candemachine.Boundary.from_cid(boundary_cidL)
