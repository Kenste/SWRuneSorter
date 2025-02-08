from src.runescorer import constants
from src.runescorer.rune import Rune, RuneStat


class Stat:
    def __init__(self, stat: constants.Stat):
        self._stat = stat
        self._rune_stat: RuneStat = None

    def _get_value(self) -> int:
        if self._rune_stat is None:
            raise ValueError("Trying to read the value of stat that is not present or was not checked for presence!")
        return self._rune_stat.value

    def _is_present(self, rune: Rune) -> bool:
        for sub in rune.subs:
            if sub.stat == self._stat:
                self._rune_stat = sub
                return True
        return False

    def __lt__(self, other):
        return lambda rune: self._is_present(rune) and self._get_value() < other

    def __le__(self, other):
        return lambda rune: self._is_present(rune) and self._get_value() <= other

    def __gt__(self, other):
        return lambda rune: self._is_present(rune) and self._get_value() > other

    def __ge__(self, other):
        return lambda rune: self._is_present(rune) and self._get_value() >= other

    def __eq__(self, other):
        return lambda rune: self._is_present(rune) and self._get_value() == other

    def __ne__(self, other):
        return lambda rune: self._is_present(rune) and self._get_value() != other


class ATK(Stat):
    def __init__(self):
        super().__init__(constants.Stat.ATK)


class ATK_P(Stat):
    def __init__(self):
        super().__init__(constants.Stat.ATK_P)


class DEF(Stat):
    def __init__(self):
        super().__init__(constants.Stat.DEF)


class DEF_P(Stat):
    def __init__(self):
        super().__init__(constants.Stat.DEF_P)


class HP(Stat):
    def __init__(self):
        super().__init__(constants.Stat.HP)


class HP_P(Stat):
    def __init__(self):
        super().__init__(constants.Stat.HP_P)


class SPD(Stat):
    def __init__(self):
        super().__init__(constants.Stat.SPD)


class CRate(Stat):
    def __init__(self):
        super().__init__(constants.Stat.CRate)


class CDmg(Stat):
    def __init__(self):
        super().__init__(constants.Stat.CDmg)


class RES(Stat):
    def __init__(self):
        super().__init__(constants.Stat.RES)


class ACC(Stat):
    def __init__(self):
        super().__init__(constants.Stat.ACC)
