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
    with open(file_path) as json_data:
        data = json.load(json_data)
        for profile in data:
            prof = WeightProfile(profile["name"],
                                 profile["stat weights"],
                                 profile["innate weights"],
                                 profile["triple roll scale"],
                                 profile["quad roll scale"])
            _profiles.append(prof)


def parse_runes(file_path: str) -> [Rune]:
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


def curr_score(rune: Rune):
    scores = [(rune.score(profile), profile.name) for profile in _profiles]
    return max(scores, key=lambda x: x[0])


def max_score(rune: Rune):
    scores = [(rune.max_score(profile), profile.name) for profile in _profiles]
    return max(scores, key=lambda x: x[0])


def min_score(rune: Rune):
    scores = [(rune.min_score(profile), profile.name) for profile in _profiles]
    return max(scores, key=lambda x: x[0])
