from __future__ import annotations

import random
from collections import Counter

from card_obj import CardObj
from cdb import Cdb


class Deck:
    occurrence_list: list[int] = []
    card_list: list[CardObj] = []
    __sample_list: list[CardObj] = []
    __indexOf: dict[CardObj, int] = {}
    size: int
    len: int

    def __init__(self, id_list: list[int], cdb: Cdb):
        cnt: Counter[CardObj] = Counter()
        for id in id_list:
            card = CardObj.from_id(id, cdb)
            cnt[card] += 1
            self.__sample_list.append(card)

        for card, occurrence in cnt.items():
            self.card_list.append(card)
            self.occurrence_list.append(occurrence)

        self.size = len(id_list)
        self.len = len(self.card_list)

        for i in range(0, self.len):
            self.__indexOf[self.card_list[i]] = i

    def simulate(self, n: int = 5) -> list[CardObj]:
        return random.sample(self.__sample_list, n)

    def __repr__(self) -> str:
        return f"{{ size: {self.size}, len: {self.len}, card_list: {self.card_list.__repr__()} }}"
