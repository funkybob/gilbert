import typing

import pytest

from gilbert.schema import Schema


def test_simple():

    class Dummy(Schema):
        foo: int
        bar: str = "string"
        baz: bool = False

    d = Dummy()

    assert d.bar == 'string'
    assert d.baz is False

    with pytest.raises(AttributeError):
        d.foo


def test_init():

    class Dummy(Schema):
        foo: int
        bar: str = "string"
        baz: bool = False

    d = Dummy(foo=1, bar='test', baz=True)

    assert d.foo == 1
    assert d.bar == 'test'
    assert d.baz is True


def test_init_fail():

    class Dummy(Schema):
        foo: int

    with pytest.raises(ValueError):
        Dummy(foo='test')


def test_set_fail():

    class Dummy(Schema):
        foo: int

    d = Dummy()
    with pytest.raises(ValueError):
        d.foo = 'test'


def test_nested():
    class Child(Schema):
        one: int = 1
        two: str = "two"

    class Parent(Schema):
        foo: int
        child: Child

    d = Parent(foo=1, child={'one': 2, 'two': '2'})

    assert d.foo == 1
    assert isinstance(d.child, Child)
    assert d.child.one == 2
    assert d.child.two == '2'


def test_optional():
    class Dummy(Schema):
        one: int = 1
        two: typing.Optional[int]

    d = Dummy(one=2, two=1)

    assert d.one == 2
    assert d.two == 1

    d = Dummy(one=2)
    assert d.one == 2

    with pytest.raises(AttributeError):
        d.two

    with pytest.raises(ValueError):
        d = Dummy(two='one')
