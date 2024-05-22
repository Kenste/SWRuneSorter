import logging

import constants
import rune
import util

profiles = []


def _find_relic(avail_stats, slot):
    # 4 rolls into stat
    max_upgrade_rolls = 1 + 4

    main = None
    innate = None
    subs = []

    # find max main stat
    max_main_i, max_main_val = util.max_index_val(avail_stats.main_scores)
    main_stat = avail_stats.avail_mains[max_main_i]
    if (main_stat not in avail_stats.avail_subs
            or max_main_val > avail_stats.innate_scores[avail_stats.sub_index(main_stat)]):
        # use this stat as a main stat
        logging.info(f"Using {main_stat} as main stat")
        main = rune.RuneStat(main_stat, max_main_val)
        avail_stats.remove_stat_option(max_main_i, substat=False)

        # find substat vs innate
        max_sub_i, max_sub_val = util.max_index_val(avail_stats.sub_scores)
        sub_stat = avail_stats.avail_subs[max_sub_i]
        max_innate_val = avail_stats.innate_scores[max_sub_i]
        if max_sub_val * max_upgrade_rolls > max_innate_val:
            # use this stat as a substat
            logging.info(f"Using {sub_stat} as initial maxed out substat")
            subs.append(rune.RuneStat(sub_stat, max_sub_val * max_upgrade_rolls))
            avail_stats.remove_stat_option(max_sub_i)

            # use max innate as innate
            max_innate_i, max_innate_val = util.max_index_val(avail_stats.innate_scores)
            innate_stat = avail_stats.avail_subs[max_innate_i]
            logging.info(f"Using {innate_stat} as innate stat")
            innate = rune.RuneStat(innate_stat, max_innate_val)
            avail_stats.remove_stat_option(max_innate_i)
        else:
            # use found substat as innate
            logging.info(f"Using {sub_stat} as innate stat")
            innate = rune.RuneStat(sub_stat, avail_stats.innate_scores[max_sub_i])
            avail_stats.remove_stat_option(max_sub_i)
    else:
        # use found main stat as innate
        max_innate_i = avail_stats.sub_index(main_stat)
        max_innate_val = avail_stats.innate_scores[max_innate_i]
        logging.info(f"Using {main_stat} as innate stat")
        innate = rune.RuneStat(main_stat, max_innate_val)
        avail_stats.remove_stat_option(max_innate_i)

        # find a new main stat
        max_main_i, max_main_val = util.max_index_val(avail_stats.main_scores)
        main_stat = avail_stats.avail_mains[max_main_i]
        logging.info(f"Using {main_stat} as main stat")
        main = rune.RuneStat(main_stat, max_main_val)
        avail_stats.remove_stat_option(max_main_i, substat=False)

    # fill remaining substats
    for j in range(len(subs), 4):
        max_sub_i, max_sub_val = util.max_index_val(avail_stats.sub_scores)
        if len(subs) == 0:
            logging.info(f"Using {avail_stats.avail_subs[max_sub_i]} as maxed out substat")
            subs.append(rune.RuneStat(avail_stats.avail_subs[max_sub_i], max_sub_val * max_upgrade_rolls))
        else:
            logging.info(f"Adding {avail_stats.avail_subs[max_sub_i]} as substat")
            subs.append(rune.RuneStat(avail_stats.avail_subs[max_sub_i], max_sub_val))
        avail_stats.remove_stat_option(max_sub_i)
    return rune.Rune(main, innate, subs, 15, slot, constants.Quality.Legend)


class WeightProfile:
    def __init__(self, name, stat_weights, innate_weights, triple_roll_bonus, quad_roll_bonus):
        """
        :param name: the name to identify this weight profile
        :param stat_weights: a dictionary to map the stat to a weight
        :param innate_weights: a dictionary to map the (innate) stat to a weight
        :param triple_roll_bonus: the bonus to add to the triple rolled stat
        :param quad_roll_bonus: the bonus to add to the quad rolled stat
        """
        self.name = name
        self.stat_weights = stat_weights
        self.innate_weights = innate_weights
        self.triple_roll_bonus = max(triple_roll_bonus, 0)
        self.quad_roll_bonus = max(quad_roll_bonus, 0)
        self.factors = []
        profiles.append(self)
        self.normalize(stat_weights, innate_weights)

    def get_normalization_factor(self, slot):
        if len(self.factors) < 6:
            return 1
        return self.factors[slot - 1]

    def normalize(self, stat_weights, innate_weights):
        logging.info(f"Normalizing WeightProfile {self.name}")
        for slot in range(1, 7):
            avail_stats = util.AvailableStatsAndScore(slot, self)
            r = _find_relic(avail_stats, slot)
            max_score = r.score(self)
            normalization_factor = 100 / max_score
            self.factors.append(normalization_factor)
            logging.info(f"Normalized slot {slot} with score {max_score} and factor {normalization_factor}")
