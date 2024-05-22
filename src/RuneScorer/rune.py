import constants
import math
import logging
from weight import WeightProfile


class RuneStat:
    def __init__(self, stat: constants.Stat, value: int):
        self.stat = stat
        self.value = value

    def score(self, profile: WeightProfile, innate=False, main=False) -> float:
        """
        Returns the score for this rune stat.
        :param profile: the weight profile to use for the score calculation
        :param innate: whether this stat is an innate stat or not
        :param main: whether this stat is a main stat or not
        :return: the score of this rune stat
        """
        if innate:
            res = self.value * profile.innate_weights.get(self.stat)
            logging.info(f"{self.stat} is scored as innate with weight {profile.innate_weights.get(self.stat)} and result {res}")
            return res

        avg_roll_count = self.get_roll_count()
        if not main and avg_roll_count >= 4:
            roll_count_bonus = profile.quad_roll_bonus
        elif not main and avg_roll_count >= 3:
            roll_count_bonus = profile.triple_roll_bonus
        else:
            roll_count_bonus = 0

        weight = profile.stat_weights.get(self.stat)
        res = self.value * (weight + roll_count_bonus)
        logging.info(f"{self.stat} is scored with weight {profile.innate_weights.get(self.stat)}, roll bonus {roll_count_bonus} and result {res}")
        return res

    def get_roll_count(self) -> int:
        """
        Returns the number of average upgrade rolls that went into this stat.
        :return: the number of upgrade rolls that went into this stat
        """
        upgrade_range = constants.sub_upgrade_range.get(self.stat)
        avg = sum(upgrade_range) / len(upgrade_range)
        return math.floor(self.value / avg) - 1


class Rune:
    def __init__(self, main: RuneStat, innate: RuneStat, subs: [RuneStat], level: int, slot: int,
                 quality: constants.Quality):
        self.main = main
        self.innate = innate
        self.subs = subs
        self.level = level
        self.slot = slot
        self.quality = quality

    def score(self, profile):
        main_score = self.main.score(profile, main=True)
        innate_score = self.innate.score(profile, innate=True)
        sub_scores = [sub.score(profile) for sub in self.subs]
        return (main_score + innate_score + sum(sub_scores)) * profile.get_normalization_factor(self.slot)
