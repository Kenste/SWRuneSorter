import constants
import math
import logging
from copy import copy


def _add_new_stat(rune, profile, eval_func):
    stats = [sub.stat for sub in rune.subs]
    avail_stats = [stat for stat in constants.slot_to_available_substat.get(rune.slot) if stat not in stats]
    stat_scores = [(stat, eval_func(constants.sub_upgrade_range.get(stat)) * profile.stat_weights.get(stat)) for stat in
                   avail_stats]
    stat = eval_func(stat_scores, key=lambda x: x[1])[0]
    rune.subs.append(RuneStat(stat, eval_func(constants.sub_upgrade_range.get(stat))))


def _upgrade_max_potential_stat(rune, profile):
    subs = []
    for sub in rune.subs:
        max_sub = copy(sub)
        upper_upgrade = constants.sub_upgrade_range.get(max_sub.stat)[1]
        max_sub.value += rune.remaining_upgrades() * upper_upgrade
        subs.append((max_sub, max_sub.score(profile)))
    max_sub = max(subs, key=lambda x: x[1])
    i = subs.index(max_sub)
    rune.subs[i].value = max_sub[0].value


def _upgrade_min_potential_stats(rune, profile):
    res = copy(rune)
    for _ in range(rune.remaining_upgrades()):
        # upgrade each stat separate
        variants_score = []
        for i in range(len(rune.subs)):
            curr = copy(res)
            curr.subs[i].value += constants.sub_upgrade_range.get(curr.subs[i].stat)[0]
            variants_score.append((curr, curr.score(profile)))
        # find min scoring rune
        res = min(variants_score, key=lambda x: x[1])[0]
    rune.subs = res.subs


def _max_main_stat(rune):
    main = rune.main
    max_main_val = constants.primary_upgrade_changes.get(main.stat)[2]
    main.value = max_main_val
    rune.level = 15


class RuneStat:
    def __init__(self, stat: constants.Stat, value: int):
        self.stat = stat
        self.value = value

    def score(self, profile, innate=False, main=False) -> float:
        """
        Returns the score for this rune stat.
        :param profile: the weight profile to use for the score calculation
        :param innate: whether this stat is an innate stat or not
        :param main: whether this stat is a main stat or not
        :return: the score of this rune stat
        """
        if innate:
            res = self.value * profile.innate_weights.get(self.stat)
            logging.info(
                f"{self.stat} is scored as innate with weight {profile.innate_weights.get(self.stat)} and result {res}")
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
        logging.info(
            f"{self.stat} is scored with weight {profile.innate_weights.get(self.stat)}, roll bonus {roll_count_bonus} and result {res}")
        return res

    def __copy__(self):
        return RuneStat(self.stat, self.value)

    def __str__(self):
        return f"{self.stat, self.value}"

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
        innate_score = self.innate.score(profile, innate=True) if self.innate is not None else 0
        sub_scores = [sub.score(profile) for sub in self.subs]
        return (main_score + innate_score + sum(sub_scores)) * profile.get_normalization_factor(self.slot)

    def remaining_upgrades(self):
        remaining = max(math.ceil((12 - self.level) / 3), 0)
        if self.quality == constants.Quality.Hero:
            remaining = max(remaining - 1, 0)
        return remaining

    def max_score(self, profile):
        max_rune = copy(self)
        _upgrade_max_potential_stat(max_rune, profile)
        if max_rune.quality == constants.Quality.Hero:
            _add_new_stat(max_rune, profile, max)
        _max_main_stat(max_rune)
        return max_rune.score(profile)

    def min_score(self, profile):
        min_rune = copy(self)
        _upgrade_min_potential_stats(min_rune, profile)
        if min_rune.quality == constants.Quality.Hero:
            _add_new_stat(min_rune, profile, min)
        _max_main_stat(min_rune)
        return min_rune.score(profile)

    def __copy__(self):
        return Rune(copy(self.main), copy(self.innate), [copy(sub) for sub in self.subs], self.level, self.slot,
                    self.quality)

    def __str__(self):
        return f"{self.main}, {self.innate}, {[str(sub) for sub in self.subs]}, {self.level}, {self.slot}, {self.quality}"
