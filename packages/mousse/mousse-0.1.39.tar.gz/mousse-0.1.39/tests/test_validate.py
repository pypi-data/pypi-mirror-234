from typing import *

from mousse import Dataclass, validate

Number = Union[int, float]


class Foo(Dataclass):
    name: str
    number: float
    items: List[str] = []


def test_validate():
    assert validate(int, 1)
    assert not validate(int, 1.0)

    assert validate(Number, 1)
    assert validate(Number, 1.0)

    assert validate(Dict[str, Any], {"a": 1, "b": "a"})

    assert not validate(Dict[str, int], {"a": 1, "b": "a"})

    assert validate(Tuple[int, float], (1, 1.2))
    assert not validate(Tuple[int, float], (1.0, 1.2))
    assert validate(Tuple[Number, Number], (1, 1.2))

    foo = Foo(name="foo", number=42.0, items=["banana", "egg"])
    assert validate(Foo, foo)
    assert validate(Foo, {"name": "foo", "number": 42.0}, as_schema=True)
    assert validate(List[Foo], [foo])
    assert not validate(List[Foo], (foo,))
    assert validate(Sequence[Foo], (foo,))
    assert validate(Tuple[Foo, ...], (foo,))
