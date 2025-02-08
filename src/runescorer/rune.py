from typing import List

from src.runescorer.constants import Stat, Quality


class RuneStat:
    def __init__(self, stat: Stat, value: int):
        self.stat = stat
        self.value = value

    def __str__(self):
        return f"{self.stat, self.value}"


class Rune:
    def __init__(self, main: RuneStat, innate: RuneStat, subs: List[RuneStat], level: int, slot: int,
                 quality: Quality, set: str, stars: int):
        self.set = set
        self.level = level
        self.quality = quality
        self.slot = slot
        self.stars = stars

        self.main = main
        self.innate = innate
        self.subs = subs

    def __str__(self):
        return f"{self.main}, {self.innate}, {[str(sub) for sub in self.subs]}, {self.level}, {self.slot}, {self.quality}"
