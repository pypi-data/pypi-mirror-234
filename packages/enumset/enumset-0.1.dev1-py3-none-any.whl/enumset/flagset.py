from typing import Optional, Iterable
from enum import Enum, EnumType
from logging import getLogger

_log = getLogger(__name__)


class Flagset:
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

    def _bits(self, key: str) -> tuple[int, int, EnumType]:
        _log.debug("bits: key %s", key)
        cur_bits = 0
        for k, v in self.keys:
            bits = len(v)
            if k == key:
                _log.debug("bits %s -> %s, %s, %s", key, cur_bits, bits, v)
                return cur_bits, bits, v
            cur_bits += bits
        _log.debug("notfound %s", key)
        raise KeyError(f"key {key} not found")

    def _num(self, key: str, e: Enum) -> int:
        cur_bits, _, _ = self._bits(key)
        pval = 1 << (list(type(e)).index(e))
        return pval << cur_bits

    def _mask(self, key: str) -> Optional[int]:
        cur_bits, bits, _ = self._bits(key)
        return ((1 << bits)-1) << cur_bits

    def get(self, key: str) -> Iterable[Enum]:
        _log.debug("get %s", key)
        cur_bits, bits, tp = self._bits(key)
        vval = (self.val >> cur_bits) & ((1 << bits)-1)
        for vv in list(tp):
            if (vval & 1) != 0:
                yield vv
            vval >>= 1

    def iteritems(self) -> Iterable[tuple[str, Enum]]:
        cur_val = self.val
        for k, v in self.keys:
            for vv in list(v):
                if (cur_val & 1) != 0:
                    yield k, vv
                cur_val >>= 1

    def clear(self, key: str):
        v = self._mask(key)
        self.val &= ~(v)

    def clear1(self, key: str, e: Enum):
        n = self._num(key, e)
        self.val &= ~(n)

    def set(self, key: str, e: Enum):
        n = self._num(key, e)
        self.val |= n

    def isset(self, key: str, e: Enum):
        n = self._num(key, e)
        return (self.val & n) != 0

    # value-only operations
    def iterval(self):
        for _, v in self.iteritems():
            yield v

    def getval(self, et: EnumType) -> Iterable[Enum]:
        k = self._getkey(et)
        return self.get(k)

    def clearval(self, et: EnumType):
        k = self._getkey(et)
        return self.clear(k)

    def clearval1(self, e: Enum):
        k = self._getkey(type(e))
        return self.clear1(k, e)

    def setval(self, n: Enum):
        k = self._getkey(type(n))
        self.set(k, n)

    def issetval(self, n: Enum):
        k = self._getkey(type(n))
        return self.isset(k, n)
