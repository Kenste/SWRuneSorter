import logging

from runescorer import constants
from runescorer import rune
from util import available_stats


def _find_relic(avail_stats, slot: int) -> rune.Rune:
    """
    Finds a "perfect" legend rune, i.e. one that maximises the score for the profile.
    :param avail_stats: the helper class holding the scores of the stats
    :param slot: the slot to find the perfect rune for
    :return: the rune that maximises the score for the provided profile
    """
    # 4 rolls into stat
    max_upgrade_rolls = 1 + 4

    main = None
    innate = None
    subs = []

    # find max main stat
    max_main_i, max_main_score = available_stats.max_index_val(avail_stats.main_scores)
    main_stat = avail_stats.avail_mains[max_main_i]
    if (main_stat not in avail_stats.avail_subs
            or max_main_score > avail_stats.innate_scores[avail_stats.sub_index(main_stat)]):
        # use this stat as a main stat
        logging.info(f"Using {main_stat} as main stat")
        main = rune.RuneStat(main_stat, constants.primary_upgrade_changes.get(main_stat)[2])
        avail_stats.remove_stat_option(max_main_i, substat=False)

        # find substat vs innate
        max_sub_i, max_sub_score = available_stats.max_index_val(avail_stats.sub_scores)
        sub_stat = avail_stats.avail_subs[max_sub_i]
        max_innate_score = avail_stats.innate_scores[max_sub_i]
        if max_sub_score * max_upgrade_rolls > max_innate_score:
            # use this stat as a substat
            logging.info(f"Using {sub_stat} as initial maxed out substat")
            subs.append(rune.RuneStat(sub_stat, constants.sub_upgrade_range.get(sub_stat)[1] * max_upgrade_rolls))
            avail_stats.remove_stat_option(max_sub_i)

            # use max innate as innate
            max_innate_i, max_innate_score = available_stats.max_index_val(avail_stats.innate_scores)
            innate_stat = avail_stats.avail_subs[max_innate_i]
            logging.info(f"Using {innate_stat} as innate stat")
            innate = rune.RuneStat(innate_stat, constants.sub_upgrade_range.get(innate_stat)[1])
            avail_stats.remove_stat_option(max_innate_i)
        else:
            # use found substat as innate
            logging.info(f"Using {sub_stat} as innate stat")
            innate = rune.RuneStat(sub_stat, constants.sub_upgrade_range.get(sub_stat)[1])
            avail_stats.remove_stat_option(max_sub_i)
    else:
        # use found main stat as innate
        max_innate_i = avail_stats.sub_index(main_stat)
        logging.info(f"Using {main_stat} as innate stat")
        innate = rune.RuneStat(main_stat, constants.sub_upgrade_range.get(main_stat)[1])
        avail_stats.remove_stat_option(max_innate_i)

        # find a new main stat
        max_main_i, _ = available_stats.max_index_val(avail_stats.main_scores)
        main_stat = avail_stats.avail_mains[max_main_i]
        logging.info(f"Using {main_stat} as main stat")
        main = rune.RuneStat(main_stat, constants.primary_upgrade_changes.get(main_stat)[2])
        avail_stats.remove_stat_option(max_main_i, substat=False)

    # fill remaining substats
    for j in range(len(subs), 4):
        max_sub_i, _ = available_stats.max_index_val(avail_stats.sub_scores)
        stat = avail_stats.avail_subs[max_sub_i]
        if len(subs) == 0:
            logging.info(f"Using {stat} as maxed out substat")
            subs.append(rune.RuneStat(stat, constants.sub_upgrade_range.get(stat)[1] * max_upgrade_rolls))
        else:
            logging.info(f"Adding {stat} as substat")
            subs.append(rune.RuneStat(stat, constants.sub_upgrade_range.get(stat)[1]))
        avail_stats.remove_stat_option(max_sub_i)
    return rune.Rune(main, innate, subs, 12, slot, constants.Quality.Legend)


def _find_min_rune(avail_stats, slot: int, profile) -> float:
    """
    Finds a "worst" legend rune, i.e. one that minimises the score for the profile.
    :param avail_stats: the helper class holding the scores of the stats
    :param slot: the slot to find the worst rune for
    :return: the rune that minimises the score for the provided profile
    """
    # pick the lowest scoring main stat
    min_main_i, min_main_score = available_stats.min_index_val(avail_stats.main_scores)
    main_stat = avail_stats.avail_mains[min_main_i]
    logging.info(f"Using {main_stat} as worst substat")
    main = rune.RuneStat(main_stat, constants.primary_upgrade_changes.get(main_stat)[0])
    avail_stats.remove_stat_option(min_main_i, substat=False)

    # fill substats with the lowest scoring stats
    subs = []
    for j in range(len(subs), 4):
        min_sub_i, _ = available_stats.min_index_val(avail_stats.sub_scores)
        stat = avail_stats.avail_subs[min_sub_i]
        logging.info(f"Adding {stat} as substat")
        subs.append(rune.RuneStat(stat, constants.sub_upgrade_range.get(stat)[0]))
        avail_stats.remove_stat_option(min_sub_i)
    r = rune.Rune(main, None, subs, 0, slot, constants.Quality.Legend)
    return r.min_normalized_score(profile)


class WeightProfile:
    def __init__(self, name, stat_weights, innate_weights, triple_roll_scale, quad_roll_scale):
        """
        :param name: the name to identify this weight profile
        :param stat_weights: a dictionary to map the stat to a weight
        :param innate_weights: a dictionary to map the (innate) stat to a weight
        :param triple_roll_scale: the scale to multipy the triple rolled stat with
        :param quad_roll_scale: the scale to multipy the quad rolled stat with
        """
        self.name = name
        self._stat_weights = stat_weights
        self._innate_weights = innate_weights
        self._triple_roll_scale = max(triple_roll_scale, 1)
        self._quad_roll_scale = max(quad_roll_scale, 1)
        self._factors = []
        self._base_scores = []
        self._normalize()

    def get_normalization_factor(self, slot: int) -> float:
        """
        Returns the calculated normalization factor for the given slot of runes.
        The factor can (and is used) by the rune to normalize its score between 0 and 100.
        :param slot: the slot of rune to get the normalization factor for
        :return: the normalization factor of the given slot of rune
        """
        if len(self._factors) < 6:
            return 1
        return self._factors[slot - 1]

    def get_baseline_value(self, slot: int) -> float:
        if len(self._factors) < 6:
            return 0
        return self._base_scores[slot - 1]

    def get_stat_weight(self, stat: constants.Stat) -> float:
        return self._stat_weights[stat]

    def get_innate_weight(self, stat: constants.Stat) -> float:
        return self._innate_weights[stat]

    def get_quad_scale(self) -> float:
        return self._quad_roll_scale

    def get_triple_scale(self) -> float:
        return self._triple_roll_scale

    def set_stat_weight(self, stat, value) -> None:
        self._stat_weights[stat] = value
        self._normalize()

    def set_innate_weight(self, stat, value) -> None:
        self._innate_weights[stat] = value
        self._normalize()

    def set_quad_scale(self, value) -> None:
        self._quad_roll_scale = value
        self._normalize()

    def set_triple_scale(self, value) -> None:
        self._triple_roll_scale = value
        self._normalize()

    def set_name(self, name) -> None:
        self.name = name

    def to_json(self) -> dict[str, str | float | dict[str, float]]:
        return {
            "name": self.name,
            "stat_weights": self._stat_weights,
            "innate_weights": self._innate_weights,
            "triple_roll_scale": self._triple_roll_scale,
            "quad_roll_scale": self._quad_roll_scale
        }

    def _normalize(self) -> None:
        """
        Normalizes this profile by determining a "perfect" rune, i.e. one with the highest possible score for this
        profile and uses this score as a reference point for the normalization factor.
        """
        logging.info(f"Normalizing WeightProfile {self.name}")
        self._factors.clear()
        for slot in range(1, 7):
            avail_stats = available_stats.AvailableStatsAndScore(slot, self, main_score_index=0, sub_score_index=0)
            min_score = _find_min_rune(avail_stats, slot, self)
            self._base_scores.append(min_score)
            avail_stats = available_stats.AvailableStatsAndScore(slot, self)
            max_rune = _find_relic(avail_stats, slot)
            max_score = max_rune._score(self)
            normalization_factor = 100 / (max_score - min_score)
            self._factors.append(normalization_factor)
            logging.info(f"Normalized slot {slot} with score {max_score} and factor {normalization_factor}")
