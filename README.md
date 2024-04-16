# ygo-starter-py

quick and dirty script to evaluate chance of a starter hand of a yugioh deck.

## Example Usage

```python
# main.py
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
```

```shell
$ python main.py
['抽牌小丑与封锁鸟', '捕食植物 瓶子草蚁', '悲剧之惨绝戏子', '捕食植物 土瓶草蟾蜍', '捕食植物 腺毛草胡蜂', '增殖的Z', '捕食植物 毛毡伞蜥蜴', '灰流丽', '捕食植物 百合眼镜蛇', '捕食植物 蜂兰蝎', '阿尔白斯之落胤', '支索帆水手・萝玛琳', '惨绝戏之导化 阿卢绯尔', '守宝团・姬特', '赫之圣女 卡尔塔西亚', '引导之圣女 库妸㽗', '渊兽 萨罗尼尔', '黑衣龙 阿尔比昂', '惨绝戏之随兴凶剧', '捕食植物 黏菖蒲螳螂', '深渊兽 卢绯里昂', '原始生命态 尼比鲁', '融合派兵', '天底的使徒', '烙印融合', '愚蠢埋葬', '失烙印', '超融合', '墓穴指名者', '抹杀之指名者', '捕食优选结合', '烙印开幕', '烙印之气炎', '赫之烙印', '无限泡影', '捕食计划', '烙印放逐', '烙印断罪']
matches: 342
total runs: 1000
chance: 0.342
```
