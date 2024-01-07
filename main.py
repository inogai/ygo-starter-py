from __future__ import annotations

import re
from typing import Generator

from cdb import Cdb
from criteria import AnyOf, AtLeast, EachOf, Not
from deck import Deck
from evaluation import Evaluation, EvaluationOption
from selector import NameIncludes


def with_open_gen(path: str) -> Generator[str, None, None]:
    with open(path, "r") as f:
        for line in f:
            yield line

    raise EOFError


def prepare_id_list():
    result: list[int] = []
    gen = with_open_gen("input.ydk")

    # skip until (includes) #main
    while True:
        if re.match("#main", next(gen)):
            break

    while True:
        line = next(gen)
        if re.match("#", line):
            break
        else:
            result.append(int(line))

    return result


if __name__ == "__main__":
    id_list = prepare_id_list()
    cdb = Cdb()
    # cdb.get_many_by_id([81439174, 81439175])

    deck = Deck(id_list, cdb)

    print(list(map(lambda card: card.cname, deck.card_list)))

    ev = Evaluation(
        deck,
        AnyOf(
            "烙印融合",
            "导化",
            EachOf("埋", Not("悲剧")),
            EachOf("蜂兰蝎", Not("眼镜蛇")),
            EachOf("蟾蜍", "伞蜥"),
            EachOf("蟾蜍", AtLeast(NameIncludes("捕食植物", False), 3)),
        ),
        EvaluationOption(deck_size=60, default_match_cname=True),
    )
    ev.run(1000)
    # ev.test_all(NameIncludes("Branded"))
