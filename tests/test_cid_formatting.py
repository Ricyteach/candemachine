import candemachine


def test_basic_cande_cid_format(basic_cande_asd_anal_L3, basic_cande_asd_anal_L3_cid):
    assert f"{basic_cande_asd_anal_L3:cid}" == basic_cande_asd_anal_L3_cid


def test_node_cid_format(node, node_info):
    info = node_info
    result = f'   {info["num"]}     {info["x"]: >10G}{info["y"]: >10G}'
    assert format(node, 'cid') == ' ' + result
    node.last = True
    assert format(node, 'cid') == 'L' + result


def test_element_cid_format(element, element_info):
    info = element_info
    result = f'   {info["num"]}{info["i"]: >5d}{info["j"]: >5d}{info["k"]: >5d}{info["l"]: >5d}{info["mat"]: >5d}{info["step"]: >5d}'
    result += '' if element.type==0 else f'{element.type: >5d}'
    result += '' if element.death==0 else f'               {element.death: >5d}'
    assert format(element, 'cid') == ' ' + result
    element.last = True
    assert format(element, 'cid') == 'L' + result


def test_boundary_cid_format(boundary, boundary_info):
    info = boundary_info
    result = f'  {info["node"]}{info["xcode"]: >5d}{info["xvalue"]: >10G}{info["ycode"]: >5d}{info["yvalue"]: >10G}' \
        f'{info["angle"]: >10G}{info["step"]: >5d}'
    assert format(boundary, 'cid') == ' ' + result
    boundary.last = True
    assert format(boundary, 'cid') == 'L' + result
