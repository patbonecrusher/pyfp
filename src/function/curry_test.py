import pytest

from .curry import curry


def f(x: int, y: int, z: int) -> int:
    return x + y + z

def g(x: int, y: int, z: int, a: int) -> int:
    return x + y + z + a

def d(a: int, b: int = 3, c: int = 10) -> int:
    return a + b + c


def test_all_curried_all_invoked():
    fc = curry(f)
    assert fc(1)(1)(3) == 5

def test_all_curried_partial_invoked():
    fc = curry(f)
    assert fc(1)(1)(2) == 4
    assert fc(1, 1, 2) == 4
    assert fc(1, 1)(2) == 4
    assert fc(1)(1, 2) == 4

def test_all_curried_partial_invoked2():
    gc = curry(g)
    assert gc(1)(1)(2)(3) == 7
    assert gc(1, 1, 2, 3) == 7
    assert gc(1, 1, 2)(3) == 7
    assert gc(1, 1)(2, 3) == 7
    assert gc(1, 1)(2)(3) == 7
    assert gc(1)(1, 2, 3) == 7
    assert gc(1)(1, 2)(3) == 7


def test_keyword_args():
    fc = curry(f)
    assert fc(x=1, y=1, z=2) == 4
    assert fc(x=1)(y=1)(z=2) == 4
    assert fc(z=2)(x=1)(y=1) == 4          # any order by name

def test_keyword_and_positional_interleaved():
    fc = curry(f)
    assert fc(y=1)(1, 2) == 4              # y named; x, z fill positionally
    assert fc(z=10)(1, 1) == 12
    assert fc(1)(z=2)(y=1) == 4

def test_defaults_fire_on_required():
    dc = curry(d)
    assert dc(5) == 18                     # a=5, b and c defaulted
    assert dc(a=5) == 18

def test_defaults_can_be_overridden_before_required():
    dc = curry(d)
    assert dc(b=1)(c=2)(5) == 8            # optionals first, required last
    assert dc(c=2)(5) == 10               # a=5, b=3 default, c=2

def test_duplicate_argument_raises():
    fc = curry(f)
    with pytest.raises(TypeError):
        fc(1, x=5)                         # x given positionally and by name

def test_unexpected_keyword_raises():
    fc = curry(f)
    with pytest.raises(TypeError):
        fc(w=1)

def test_too_many_positional_raises():
    fc = curry(f)
    with pytest.raises(TypeError):
        fc(1, 2, 3, 4)
