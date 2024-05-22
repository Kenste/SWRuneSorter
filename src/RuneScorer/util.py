import constants


def max_index_val(l):
    return max(enumerate(l), key=lambda x: x[1])


class AvailableStatsAndScore:
    def __init__(self, slot: int, profile):
        # get available stats for this slot
        self.avail_mains = constants.slot_to_available_mainstat.get(slot).copy()
        self.avail_subs = constants.slot_to_available_substat.get(slot).copy()
        # get the max score of each stat
        self.main_scores = [profile.stat_weights.get(main) * constants.primary_upgrade_changes.get(main)[2] for main in
                            self.avail_mains]
        self.sub_scores = [profile.stat_weights.get(sub) * constants.sub_upgrade_range.get(sub)[1] for sub in
                           self.avail_subs]
        self.innate_scores = [profile.innate_weights.get(sub) * constants.sub_upgrade_range.get(sub)[1] for sub in
                              self.avail_subs]

    def remove_stat_option(self, index, substat=True):
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

    def main_index(self, stat):
        return self.avail_mains.index(stat)

    def sub_index(self, stat):
        return self.avail_subs.index(stat)
