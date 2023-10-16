from typing import Optional
from enum import Enum, EnumType
from logging import getLogger

_log = getLogger(__name__)


class Enumset:
    def __init__(self):
        self.val: int = 0
        self.keys: list[tuple[str, EnumType]] = []

    def define_enum(self, key: str, et: EnumType) -> None:
        if key is None:
            key = et.__name__
        for k, v in self.keys:
            if v == et:
                _log.warning("duplicate type: key=%s", k)
            if k == key:
                raise IndexError(f"duplicate key {key}")
        self.keys.append((key, et))

    def _getkey(self, et: EnumType) -> str:
        for k, v in self.keys:
            if v == et:
                return k
        raise KeyError(f"type {et} not found")

    def _num(self, key: str, e: Enum) -> int:
        pval = list(type(e)).index(e) + 1
        for k, v in self.keys:
            vlen = len(v) + 1
            if k == key:
                return pval
            pval *= vlen
        raise KeyError(f"key {key} not found")

    def get(self, key: str) -> Optional[Enum]:
        cur_val = self.val
        for k, v in self.keys:
            vlen = len(v) + 1
            if k == key:
                vv = cur_val % vlen
                if vv == 0:
                    return None
                return list(v)[vv-1]
            cur_val //= vlen
        raise KeyError(f"key {key} not found")

    def iteritems(self):
        cur_val = self.val
        for k, v in self.keys:
            vlen = len(v) + 1
            vv = cur_val % vlen
            if vv != 0:
                yield k, list(v)[vv-1]
            cur_val //= vlen

    def clear(self, key: str):
        v = self.get(key)
        if v is None:
            return
        n = self._num(key, v)
        self.val -= n

    def set(self, key: str, n: Enum):
        self.clear(key)
        self.val += self._num(key, n)

    # value-only operations
    def iterval(self):
        for _, v in self.iteritems():
            yield v

    def getval(self, et: EnumType) -> Optional[Enum]:
        k = self._getkey(et)
        return self.get(k)

    def clearval(self, et: EnumType):
        k = self._getkey(et)
        self.clear(k)

    def setval(self, n: Enum):
        k = self._getkey(type(n))
        self.set(k, n)
