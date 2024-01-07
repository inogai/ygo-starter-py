from __future__ import annotations

from dataclasses import dataclass

from cdb import Cdb


@dataclass
class CardObj:
    cid: int
    name: str
    cname: str

    @staticmethod
    def from_id(id: int, cdb: Cdb) -> CardObj:
        entry = cdb.get_many_by_id([id])[0]
        _cname = entry.sc_name
        if _cname == str(None):
            _cname = entry.cn_name

        return CardObj(entry.cid, entry.en_name, _cname)

    def __repr__(self) -> str:
        return f'"{self.name}"'

    def __hash__(self) -> int:
        return self.cid.__hash__()

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, CardObj):
            return False

        if self.cid == other.cid:
            return True

        return False
