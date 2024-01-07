from __future__ import annotations

import random
import re
from dataclasses import dataclass

import criteria as crit
import selector as selc
from card_obj import CardObj
from criteria import Criteria
from deck import Deck
from selector import Selector


@dataclass
class EvaluationOption:
    deck_size: int = 40
    default_match_cname: bool = False


class Evaluation:
    deck: Deck
    __card_list: list[CardObj]
    crit: Criteria

    def __init__(
        self,
        deck: Deck,
        crit: Criteria,
        option: EvaluationOption = EvaluationOption(),
    ) -> None:
        self.deck = deck
        self.crit = crit
        self.option = option

        for selector in crit.breakdown():
            if not selector.want_unique:
                continue

            lst = []
            if not self.test_unique(selector, lst):
                raise ValueError(
                    f"It has `want_unique: True`, but none/multiple card matched the selector `{selector.name}`: {lst}",
                )

        len_diff = option.deck_size - len(deck.card_list)
        if len_diff < 0:
            raise ValueError("deck_size too small!")

        self.__card_list = [
            *deck.card_list,
            *[CardObj(-1, "Template", "Template")] * len_diff,
        ]

    def run(self, n: int = 10) -> float:
        count = 0
        for _ in range(1, n):
            if self.test(self.starter_hand(), self.crit):
                count += 1

        print(f"matches: {count}")
        print(f"total runs: {n}")
        print(f"chance: {count / n}")

        return count

    def starter_hand(self, number: int = 5) -> list[CardObj]:
        return random.sample(self.__card_list, number)

    def select(self, card: CardObj, selector: Selector) -> bool:
        match selector:
            case selc.NameIncludes():
                if self.option.default_match_cname:
                    return re.search(selector.regex, card.cname) is not None

                return re.search(selector.regex, card.name) is not None

        raise TypeError("Unsupported type")

    def test(self, card_list: list[CardObj], criteria: Criteria):
        match criteria:
            case crit.Not():
                return not self.test(card_list, criteria.child)

            case crit.AnyOf():
                for child in criteria.list:
                    if self.test(card_list, child):
                        return True

                return False

            case crit.EachOf():
                for sub_crit in criteria.list:
                    if not self.test(card_list, sub_crit):
                        return False

                return True

            case crit.AtLeast():
                counter = 0
                for card in card_list:
                    if not self.select(card, criteria.selector):
                        continue

                    counter += 1
                    if counter >= criteria.number:
                        return True

                return False

            case crit.AtMost():
                counter = 0
                for card in card_list:
                    if not self.select(card, criteria.selector):
                        continue

                    counter += 1
                    if counter >= criteria.number:
                        return True

                return False

        raise TypeError("Unsupported type")

    def test_unique(self, selector: Selector, lst: list[CardObj] = []):
        if not selector.want_unique:
            return True

        lst += list(
            filter(lambda card: self.select(card, selector), self.deck.card_list)
        )
        if len(lst) == 1:
            return True

        return False
