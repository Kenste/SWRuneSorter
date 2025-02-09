from src.runescorer import constants
from src.runescorer.rune import Rune


class Stat:
    def __init__(self, stat: constants.Stat, location: constants.StatLocation):
        self._stat = stat
        self._stat_location = location

    def _get_value(self, rune: Rune) -> int:
        if self._stat_location == constants.StatLocation.Main:
            if rune.main.stat == self._stat:
                return rune.main.value

        elif self._stat_location == constants.StatLocation.Innate:
            if rune.innate.stat == self._stat:
                return rune.innate.value

        elif self._stat_location == constants.StatLocation.Sub:
            for sub in rune.subs:
                if sub.stat == self._stat:
                    return sub.value

        raise ValueError("No Value Found! Check if stat if present first!")

    def _is_present(self, rune: Rune) -> bool:
        if self._stat_location == constants.StatLocation.Main:
            if rune.main.stat == self._stat:
                self._rune_stat = rune.main
                return True

        elif self._stat_location == constants.StatLocation.Innate:
            if rune.innate.stat == self._stat:
                self._rune_stat = rune.innate
                return True

        elif self._stat_location == constants.StatLocation.Sub:
            for sub in rune.subs:
                if sub.stat == self._stat:
                    self._rune_stat = sub
                    return True

        return False

    def __lt__(self, other):
        return lambda rune: self._is_present(rune) and self._get_value(rune) < other

    def __le__(self, other):
        return lambda rune: self._is_present(rune) and self._get_value(rune) <= other

    def __gt__(self, other):
        return lambda rune: self._is_present(rune) and self._get_value(rune) > other

    def __ge__(self, other):
        return lambda rune: self._is_present(rune) and self._get_value(rune) >= other

    def __eq__(self, other):
        return lambda rune: self._is_present(rune) and (
                self._stat_location == constants.StatLocation.Main or self._get_value(rune) == other
        )

    def __ne__(self, other):
        return not self.__eq__(other)


class ATK(Stat):
    def __init__(self, location: constants.StatLocation = constants.StatLocation.Sub):
        super().__init__(constants.Stat.ATK, location)


class ATK_P(Stat):
    def __init__(self, location: constants.StatLocation = constants.StatLocation.Sub):
        super().__init__(constants.Stat.ATK_P, location)


class DEF(Stat):
    def __init__(self, location: constants.StatLocation = constants.StatLocation.Sub):
        super().__init__(constants.Stat.DEF, location)


class DEF_P(Stat):
    def __init__(self, location: constants.StatLocation = constants.StatLocation.Sub):
        super().__init__(constants.Stat.DEF_P, location)


class HP(Stat):
    def __init__(self, location: constants.StatLocation = constants.StatLocation.Sub):
        super().__init__(constants.Stat.HP, location)


class HP_P(Stat):
    def __init__(self, location: constants.StatLocation = constants.StatLocation.Sub):
        super().__init__(constants.Stat.HP_P, location)


class SPD(Stat):
    def __init__(self, location: constants.StatLocation = constants.StatLocation.Sub):
        super().__init__(constants.Stat.SPD, location)


class CRate(Stat):
    def __init__(self, location: constants.StatLocation = constants.StatLocation.Sub):
        super().__init__(constants.Stat.CRate, location)


class CDmg(Stat):
    def __init__(self, location: constants.StatLocation = constants.StatLocation.Sub):
        super().__init__(constants.Stat.CDmg, location)


class RES(Stat):
    def __init__(self, location: constants.StatLocation = constants.StatLocation.Sub):
        super().__init__(constants.Stat.RES, location)


class ACC(Stat):
    def __init__(self, location: constants.StatLocation = constants.StatLocation.Sub):
        super().__init__(constants.Stat.ACC, location)
