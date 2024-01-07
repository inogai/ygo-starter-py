from __future__ import annotations

from dataclasses import dataclass
from functools import reduce
from typing import TypeAlias

from selector import Selector, SelectorCompatible, to_selector


@dataclass
class Not:
    child: Criteria

    def __init__(self, criteria: CriteriaCompatible):
        self.child = to_criteria(criteria)

    def breakdown(self) -> list[Selector]:
        return self.child.breakdown()


@dataclass
class AnyOf:
    list: list[Criteria]

    def __init__(self, *list: CriteriaCompatible):
        self.list = [to_criteria(it) for it in list]

    def breakdown(self) -> list[Selector]:
        lst: list[Selector] = []
        return reduce(
            lambda accu, criteria: [*accu, *criteria.breakdown()], self.list, lst
        )


@dataclass
class EachOf:
    list: list[Criteria]

    def __init__(self, *list: CriteriaCompatible):
        self.list = [to_criteria(it) for it in list]

    def breakdown(self) -> list[Selector]:
        lst: list[Selector] = []
        return reduce(
            lambda accu, criteria: [*accu, *criteria.breakdown()], self.list, lst
        )


@dataclass
class AtLeast:
    selector: Selector
    number: int

    def __init__(self, selector: SelectorCompatible, number: int):
        self.selector = to_selector(selector)
        self.number = number

    def breakdown(self) -> list[Selector]:
        return [self.selector]


@dataclass
class AtMost:
    selector: Selector
    number: int

    def breakdown(self) -> list[Selector]:
        return [self.selector]


Criteria: TypeAlias = Not | AnyOf | EachOf | AtLeast | AtMost
CriteriaCompatible: TypeAlias = str | Selector | Criteria


def to_criteria(obj: CriteriaCompatible) -> Criteria:
    if isinstance(obj, str):
        obj = to_selector(obj)

    if isinstance(obj, Selector):
        return AtLeast(obj, 1)

    return obj
