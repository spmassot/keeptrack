import src.data_utils as du


class A:
    def __init__(self, prop1, prop2, b_id):
        self.prop1 = prop1
        self.prop2 = prop2
        self.b_id = b_id


class B:
    def __init__(self, prop3, prop4, id):
        self.prop3 = prop3
        self.prop4 = prop4
        self.id = id


def test_left_join():
    As = [A(1, 2, 'b_1'), A(11, 22, 'b_2')]
    Bs = [B(3, 4, 'b_1'), B(33, 44, 'b_2')]

    new_As = du.left_join(As, 'b_id', Bs, 'id', ['prop3', 'prop4'])
    assert new_As[0].prop1 == 1
    assert new_As[0].prop2 == 2
    assert new_As[0].B_prop3 == 3
    assert new_As[0].B_prop4 == 4
    assert new_As[0].b_id == 'b_1'

    assert new_As[1].prop1 == 11
    assert new_As[1].prop2 == 22
    assert new_As[1].B_prop3 == 33
    assert new_As[1].B_prop4 == 44
    assert new_As[1].b_id == 'b_2'
