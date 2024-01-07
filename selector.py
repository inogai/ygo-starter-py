import re
from typing import TypeAlias


class NameIncludes:
    """
    The very basic `CardSelector`. Match if the card name includes a substring.

    Args:
        pattern (str): the string to match. not case-sensitive.
        wantsUnique (bool): defaults to `True`. The parser will panic if multiple/none cards match this selector.
    """

    regex: re.Pattern[str]
    want_unique: bool
    name: str

    def __init__(self, pattern: str, wants_unique: bool = True):
        self.regex = re.compile(pattern, re.IGNORECASE)
        self.want_unique = wants_unique
        self.name = pattern


Selector: TypeAlias = NameIncludes
SelectorCompatible: TypeAlias = str | Selector


def to_selector(obj: str | Selector) -> Selector:
    if isinstance(obj, str):
        return Selector(obj, True)

    return obj
