from app import add, multiply

def test_add():
    assert add(3, 5) == 8
    assert add(-1, 1) == 0

def test_multiply():
    assert multiply(4, 3) == 12
    assert multiply(0, 5) == 0