import json

from runescorer.constants import Quality, Stat
from runescorer.rune import Rune, RuneStat
from runescorer.weight import WeightProfile

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


def weight_profiles_from_json(file_path: str) -> [WeightProfile]:
    """
    Deserializes the weight profiles given in the provided file.
    :param file_path: the path to the file
    :return: all parsed weight profiles
    """
    with open(file_path, "r") as file:
        data = json.load(file)
        return [WeightProfile(**profile_data) for profile_data in data]


def profiles_to_json(file_path: str, profiles: [WeightProfile]) -> None:
    """
    Serializes the given weight profiles as JSON into the provided file.
    :param file_path: the file to write the serialized weight profiles
    :param profiles: the weight profiles to serialize
    """
    with open(file_path, "w") as file:
        data = json.dumps([profile.to_json() for profile in profiles], indent=2)
        file.write(data)


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
