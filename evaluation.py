from __future__ import annotations
import math
from typing import TypeAlias

import random
import re
from dataclasses import dataclass

import criteria
import selector
from card_obj import CardObj
from criteria import Criteria
from deck import Deck
from selector import Selector


@dataclass
class EvaluationOption:
    deck_size: int = 40
    default_match_cname: bool = False


@dataclass
class Wish:
    criteria: Criteria
    list: list[CardObj]
    amount: int


Wishes: TypeAlias = list[Wish]


class Evaluation:
    deck: Deck
    __card_list: list[CardObj]
    criteria: Criteria
    __wish: dict[Criteria, Wishes]
    __deck_size: int

    def __init__(
        self,
        deck: Deck,
        criteria: Criteria,
        option: EvaluationOption = EvaluationOption(),
    ) -> None:
        self.deck = deck
        self.criteria = criteria
        self.option = option
        self.__deck_size = option.deck_size

        for selc in criteria.breakdown():
            if not selc.want_unique:
                continue

            lst = []
            if not self.test_unique(selc, lst):
                raise ValueError(
                    f"It has `want_unique: True`, but none/multiple card matched the selc `{selc.name}`: {lst}",
                )

        len_diff = self.__deck_size - len(deck.card_list)
        if len_diff < 0:
            raise ValueError("deck_size too small!")

        self.__card_list = [
            *deck.card_list,
            *[CardObj(-1, "Template", "Template")] * len_diff,
        ]

    def run(self, n: int = 10) -> float:
        count = 0
        for _ in range(1, n):
            if self.test(self.starter_hand(), self.criteria):
                count += 1

        print(f"matches: {count}")
        print(f"total runs: {n}")
        print(f"chance: {count / n}")

        return count

    def starter_hand(self, number: int = 5) -> list[CardObj]:
        return random.sample(self.__card_list, number)

    def select(self, card: CardObj, selc: Selector) -> bool:
        match selc:
            case selector.NameIncludes():
                if self.option.default_match_cname:
                    return re.search(selc.regex, card.cname) is not None

                return re.search(selc.regex, card.name) is not None

        raise TypeError("Unsupported type")

    def get_cards_by_selector(self, selc: Selector) -> list[CardObj]:
        return list(filter(lambda card: self.select(card, selc), self.deck.card_list))

    def __comb_wish(self, a: Wish) -> int:
        return math.comb(len(a.list), a.amount)

    def __comb_left(self, choices: int, amount: int, n: int) -> int:
        return math.comb(self.__deck_size - choices, n - amount)

    def __comb_total(self, n: int) -> int:
        return math.comb(self.__deck_size, n)

    def chance(self, a: Wish, n: int = 5):
        return (
            self.__comb_wish(a)
            * self.__comb_left(len(a.list), a.amount, n)
            / self.__comb_total(n)
        )

    def __chance_and_with_no_intersects(self, a: Wish, b: Wish, n: int = 5):
        return (
            self.__comb_wish(a)
            * self.__comb_wish(b)
            * self.__comb_left(len(a.list) + len(b.list), a.amount + b.amount, n)
            / self.__comb_total(n)
        )

    def merge_wishes(self, a: Wish, b: Wish):
        #   P(A+B = 1 and B+C = 1)
        # = P(B = 1 OR (NOT B=1 and A=1 and C=1))
        a_intersect_b = set(a.list) - set(b.list)
        # hey check how set works, make wishes store identical data of copies of card
        # i.e. indices

    def evalnew(self, crit: Criteria):
        match crit:
            case criteria.AtLeast():
                lst = self.get_cards_by_selector(crit.selector)
                self.__wish[crit] = [Wish(crit, lst, i) for i in range(crit.number, 4)]
            case _:
                raise NotImplementedError

    def test(self, card_list: list[CardObj], crit: Criteria):
        match crit:
            case criteria.Not():
                return not self.test(card_list, crit.child)

            case criteria.AnyOf():
                for child in crit.list:
                    if self.test(card_list, child):
                        return True

                return False

            case criteria.EachOf():
                for sub_crit in crit.list:
                    if not self.test(card_list, sub_crit):
                        return False

                return True

            case criteria.AtLeast():
                counter = 0
                for card in card_list:
                    if not self.select(card, crit.selector):
                        continue

                    counter += 1
                    if counter >= crit.number:
                        return True

                return False

            case criteria.AtMost():
                counter = 0
                for card in card_list:
                    if not self.select(card, crit.selector):
                        continue

                    counter += 1
                    if counter >= crit.number:
                        return True

                return False

        raise TypeError("Unsupported type")

    def test_unique(self, selc: Selector, lst: list[CardObj] = []):
        if not selc.want_unique:
            return True

        lst += self.get_cards_by_selector(selc)
        if len(lst) == 1:
            return True

        return False
