from typing import *

from mousse import Dataclass, Field, asclass, asdict


class Foo(Dataclass):
    name: str
    number: float
    items: List[str] = []


class Bar(Dataclass):
    foos: List[Foo]
    index: int = Field(..., alias="id")


def test_asclass():
    foo_data = {"name": "datnh21", "number": 42, "items": ["banana", "egg"]}
    foo = asclass(Foo, foo_data)

    assert foo.name == "datnh21"
    assert type(foo.number) is float
    assert len(foo.items) == len(foo_data["items"])

    bar_data = {"foos": [foo_data], "id": 1}
    bar = asclass(Bar, bar_data)

    assert bar.index == 1

    assert len(bar.foos) == 1
    for foo in bar.foos:
        assert type(foo) is Foo
