from __future__ import annotations

import json
from dataclasses import dataclass
from io import BytesIO
from typing import Any
from urllib.request import urlopen
from zipfile import ZipFile

API_URL = "https://ygocdb.com/api/v0/cards.zip"
CDB_FILE_DIR = "cache/"
CDB_FILE_PATH = "cache/cards.json"


@dataclass
class CdbEntry:
    cid: int
    id: int
    cn_name: str
    sc_name: str
    md_name: str
    nwbbs_n: str
    cnocg_n: str
    jp_ruby: str
    jp_name: str
    en_name: str
    text: Text
    data: Data

    @staticmethod
    def from_dict(obj: Any) -> CdbEntry:
        _cid = int(obj.get("cid"))
        _id = int(obj.get("id"))
        _cn_name = str(obj.get("cn_name"))
        _sc_name = str(obj.get("sc_name"))
        _md_name = str(obj.get("md_name"))
        _nwbbs_n = str(obj.get("nwbbs_n"))
        _cnocg_n = str(obj.get("cnocg_n"))
        _jp_ruby = str(obj.get("jp_ruby"))
        _jp_name = str(obj.get("jp_name"))
        _en_name = str(obj.get("en_name"))
        _text = Text.from_dict(obj.get("text"))
        _data = Data.from_dict(obj.get("data"))
        return CdbEntry(
            _cid,
            _id,
            _cn_name,
            _sc_name,
            _md_name,
            _nwbbs_n,
            _cnocg_n,
            _jp_ruby,
            _jp_name,
            _en_name,
            _text,
            _data,
        )


@dataclass
class Data:
    ot: int
    setcode: int
    type: int
    atk: int
    def_: int
    level: int
    race: int
    attribute: int

    @staticmethod
    def from_dict(obj: Any) -> "Data":
        _ot = int(obj.get("ot"))
        _setcode = int(obj.get("setcode"))
        _type = int(obj.get("type"))
        _atk = int(obj.get("atk"))
        _def = int(obj.get("def"))
        _level = int(obj.get("level"))
        _race = int(obj.get("race"))
        _attribute = int(obj.get("attribute"))
        return Data(_ot, _setcode, _type, _atk, _def, _level, _race, _attribute)


@dataclass
class Text:
    types: str
    pdesc: str
    desc: str

    @staticmethod
    def from_dict(obj: Any) -> "Text":
        _types = str(obj.get("types"))
        _pdesc = str(obj.get("pdesc"))
        _desc = str(obj.get("desc"))
        return Text(_types, _pdesc, _desc)


# Example Usage
# jsonstring = json.loads(myjsonstring)
# root = Root.from_dict(jsonstring)


class Cdb:
    __dict: dict[str, Any]

    def __init__(self) -> None:
        try:
            f = open(CDB_FILE_PATH)
            self.__dict = json.load(f)
            f.close()
        except FileNotFoundError:
            self.load_zip()
            with open(CDB_FILE_PATH) as f:
                self.__dict = json.load(f)

    def load_zip(self):
        with urlopen(API_URL) as zipresp:
            with ZipFile(BytesIO(zipresp.read())) as zfile:
                zfile.extractall(CDB_FILE_DIR)

    def get(self, key: str):
        value = self.__dict[key]
        return CdbEntry.from_dict(value)

    def __get_many_by_id_dangerously(self, id_list: list[int]) -> dict[int, CdbEntry]:
        if len(id_list) == 0:
            raise ValueError("`id_list` cannot have length 0")

        result: dict[int, CdbEntry] = {}

        for value in self.__dict.values():
            try:
                index = id_list.index(value["id"])
            except ValueError:
                continue

            result[index] = CdbEntry.from_dict(value)

        return result

    def get_many_by_id(self, id_list: list[int]) -> dict[int, CdbEntry]:
        result: dict[int, CdbEntry] = self.__get_many_by_id_dangerously(id_list)

        if len(result) == len(id_list):
            return result

        if len(id_list) != len(set(id_list)):
            raise ValueError("Duplicates exist! Refuse to query.")

        keys_to_find_alt_art: list[int] = list(range(0, len(id_list)) - result.keys())

        alt_id_list = [
            id_list[index] - offset
            for index in keys_to_find_alt_art
            for offset in range(1, 11)
        ]

        alt_result = self.__get_many_by_id_dangerously(alt_id_list)

        for alt_key, value in alt_result.items():
            real_key = keys_to_find_alt_art[alt_key // 10]
            result[real_key] = value

        return result
