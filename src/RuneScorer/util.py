import constants


def max_index_val(l: [int]) -> tuple[int, int]:
    """
    Returns the maximum value and its index in the given list.
    :param l: the list
    :return: the maximum value and its index in the given list as (index, value)
    """
    return max(enumerate(l), key=lambda x: x[1])


def min_index_val(l: [int]) -> tuple[int, int]:
    """
    Returns the minimum value and its index in the given list.
    :param l: the list
    :return: the minimum value and its index in the given list as (index, value)
    """
    return min(enumerate(l), key=lambda x: x[1])


class AvailableStatsAndScore:
    def __init__(self, slot: int, profile, main_score_index=2, sub_score_index=1):
        # get available stats for this slot
        self.avail_mains = constants.slot_to_available_mainstat.get(slot).copy()
        self.avail_subs = constants.slot_to_available_substat.get(slot).copy()
        # get the max score of each stat
        self.main_scores = [profile.stat_weights.get(main) *
                            constants.primary_upgrade_changes.get(main)[main_score_index] for main in self.avail_mains]
        self.sub_scores = [profile.stat_weights.get(sub) *
                           constants.sub_upgrade_range.get(sub)[sub_score_index] for sub in self.avail_subs]
        self.innate_scores = [profile.innate_weights.get(sub) *
                              constants.sub_upgrade_range.get(sub)[sub_score_index] for sub in self.avail_subs]

    def remove_stat_option(self, index, substat=True) -> None:
        """
        Removes the stat at the given index as an option from the lists.
        :param index: the index to remove the stat from
        :param substat: whether the stat is a substat or not
        """
        if substat:
            stat = self.avail_subs[index]
            if stat in self.avail_mains:
                i = self.avail_mains.index(stat)
                del self.avail_mains[i]
                del self.main_scores[i]
            del self.avail_subs[index]
            del self.sub_scores[index]
            del self.innate_scores[index]
        else:
            stat = self.avail_mains[index]
            if stat in self.avail_subs:
                i = self.avail_subs.index(stat)
                del self.avail_subs[i]
                del self.sub_scores[i]
                del self.innate_scores[i]
            del self.avail_mains[index]
            del self.main_scores[index]

    def main_index(self, stat) -> int:
        """
        Returns the index of the given stat in the main stat list.
        :param stat: the stat to get the index for
        :return: the index of the given stat in the main stat list
        """
        return self.avail_mains.index(stat)

    def sub_index(self, stat) -> int:
        """
        Returns the index of the given stat in the substat list.
        :param stat: the stat to get the index for
        :return: the index of the given stat in the substat list
        """
        return self.avail_subs.index(stat)
