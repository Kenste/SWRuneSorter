from typing import List, Callable

from runescorer.rune import Rune
from runescorer import constants


class Level:
    def __lt__(self, other: int) -> Callable[[Rune], bool]:
        return lambda rune: rune.level < other

    def __le__(self, other: int) -> Callable[[Rune], bool]:
        return lambda rune: rune.level <= other

    def __gt__(self, other: int)  -> Callable[[Rune], bool]:
        return lambda rune: rune.level > other

    def __ge__(self, other: int) -> Callable[[Rune], bool]:
        return lambda rune: rune.level >= other

    def __eq__(self, other: int) -> Callable[[Rune], bool]:
        return lambda rune: rune.level == other

    def __ne__(self, other: int) -> Callable[[Rune], bool]:
        return lambda rune: rune.level != other

    def InRange(self, lower: int, upper: int) -> Callable[[Rune], bool]:
        """
        Inclusive range.
        """
        return lambda rune: rune.level in range(lower, upper + 1)


class Quality:
    def __eq__(self, other: constants.Quality) -> Callable[[Rune], bool]:
        return lambda rune: rune.quality == other

    def __ne__(self, other: constants.Quality) -> Callable[[Rune], bool]:
        return lambda rune: rune.quality != other


class Stars:
    def __lt__(self, other: int) -> Callable[[Rune], bool]:
        return lambda rune: rune.stars < other

    def __le__(self, other: int) -> Callable[[Rune], bool]:
        return lambda rune: rune.stars <= other

    def __gt__(self, other: int) -> Callable[[Rune], bool]:
        return lambda rune: rune.stars > other

    def __ge__(self, other: int) -> Callable[[Rune], bool]:
        return lambda rune: rune.stars >= other

    def __eq__(self, other: int) -> Callable[[Rune], bool]:
        return lambda rune: rune.stars == other

    def __ne__(self, other: int) -> Callable[[Rune], bool]:
        return lambda rune: rune.stars != other


class Slot:
    def __eq__(self, other: int) -> Callable[[Rune], bool]:
        return lambda rune: rune.slot == other

    def __ne__(self, other: int) -> Callable[[Rune], bool]:
        return lambda rune: rune.slot != other

    def In(self, slots: List[int]) -> Callable[[Rune], bool]:
        return lambda rune: rune.slot in slots


class Set:
    def __eq__(self, other: str) -> Callable[[Rune], bool]:
        return lambda rune: rune.set == other

    def __ne__(self, other: str) -> Callable[[Rune], bool]:
        return lambda rune: rune.set != other

    def In(self, sets: List[str]) -> Callable[[Rune], bool]:
        return lambda rune: rune.set in sets
