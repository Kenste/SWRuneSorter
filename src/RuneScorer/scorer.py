import json

from constants import Stat, Quality
from rune import Rune, RuneStat
from weight import WeightProfile

_profiles = []
_stat_ID = [
    "null",
    Stat.HP,
    Stat.HP_P,
    Stat.ATK,
    Stat.ATK_P,
    Stat.DEF,
    Stat.DEF_P,
    "null",
    Stat.SPD,
    Stat.CRate,
    Stat.CDmg,
    Stat.RES,
    Stat.ACC
]


def parse_profiles(file_path: str) -> None:
    """
    Parses each weight profile defined in the given json file.
    :param file_path: the path to the json file containing the weight profile definitions.
    """
    with open(file_path) as json_data:
        data = json.load(json_data)
        for profile in data:
            prof = WeightProfile(profile["name"],
                                 profile["stat weights"],
                                 profile["innate weights"],
                                 profile["triple roll scale"],
                                 profile["quad roll scale"])
            _profiles.append(prof)


def parse_runes_from_json(file_path: str) -> [Rune]:
    """
    Parses every rune given in the account json file.
    :param file_path: the path to the json file
    :return: every parsed rune given in the account json file
    """
    with open(file_path) as json_data:
        data = json.load(json_data)
        runes_data = data["runes"]
        runes = []
        for rune_data in runes_data:
            level = rune_data["upgrade_curr"]
            slot = rune_data["slot_no"]
            quality = Quality.Legend if rune_data["rank"] == 5 else Quality.Hero
            main = RuneStat(_stat_ID[rune_data["pri_eff"][0]], rune_data["pri_eff"][1])
            innate = rune_data["prefix_eff"]
            if len(innate) != 0 and innate[0] != 0:
                innate = RuneStat(_stat_ID[innate[0]], innate[1])
            else:
                innate = None
            subs_data = rune_data["sec_eff"]
            subs = []
            for sub in subs_data:
                subs.append(RuneStat(_stat_ID[sub[0]], sub[1]))
            runes.append(Rune(main, innate, subs, level, slot, quality))
    return runes


def curr_score(rune: Rune) -> tuple[float, str]:
    """
    Calculates the current score of the given rune using each parsed profile.
    Returns the maximum score for the given rune as well as the name of the profile the rune scored highest with.
    :param rune: the rune to score
    :return: the max current score for the given rune as well as the name of the profile
    """
    scores = [(rune.normalized_score(profile), profile.name) for profile in _profiles]
    return max(scores, key=lambda x: x[0])


def max_score(rune: Rune) -> tuple[float, str]:
    """
    Calculates the maximum score of the given rune using each parsed profile.
    Returns the maximum score for the given rune as well as the name of the profile the rune scored highest with.
    :param rune: the rune to score
    :return: the max maximum score for the given rune as well as the name of the profile
    """
    scores = [(rune.max_normalized_score(profile), profile.name) for profile in _profiles]
    return max(scores, key=lambda x: x[0])


def min_score(rune: Rune) -> tuple[float, str]:
    """
    Calculates the minimum score of the given rune using each parsed profile.
    Returns the maximum score for the given rune as well as the name of the profile the rune scored highest with.
    The maximum score is used because it shows the "best" worst-case the rune can achieve.
    :param rune: the rune to score
    :return: the max minimum score for the given rune as well as the name of the profile
    """
    scores = [(rune.min_normalized_score(profile), profile.name) for profile in _profiles]
    return max(scores, key=lambda x: x[0])
