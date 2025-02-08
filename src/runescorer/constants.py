from enum import StrEnum


class StatLocation(StrEnum):
    Main = "Main"
    Innate = "Innate"
    Sub = "Sub"


class Stat(StrEnum):
    ATK = "ATK"
    ATK_P = "ATK%"
    DEF = "DEF"
    DEF_P = "DEF%"
    HP = "HP"
    HP_P = "HP%"
    SPD = "SPD"
    CRate = "CRate"
    CDmg = "CDmg"
    RES = "RES"
    ACC = "ACC"


class Quality(StrEnum):
    Legend = "Legend"
    Hero = "Hero"


# (lower, upper)
sub_upgrade_range = {
    Stat.ATK: (10, 20),
    Stat.ATK_P: (5, 8),
    Stat.DEF: (10, 20),
    Stat.DEF_P: (5, 8),
    Stat.HP: (135, 375),
    Stat.HP_P: (5, 8),
    Stat.SPD: (4, 6),
    Stat.CRate: (4, 6),
    Stat.CDmg: (4, 7),
    Stat.RES: (4, 8),
    Stat.ACC: (4, 8)
}

# (start value, upgrade per level, +12 value)
primary_upgrade_changes = {
    Stat.ATK: (22, 8, 118),
    Stat.ATK_P: (11, 3, 47),
    Stat.DEF: (22, 8, 118),
    Stat.DEF_P: (11, 3, 47),
    Stat.HP: (360, 120, 1800),
    Stat.HP_P: (11, 3, 47),
    Stat.SPD: (7, 2, 31),
    Stat.CRate: (7, 3, 43),
    Stat.CDmg: (11, 4, 59),
    Stat.RES: (12, 3, 48),
    Stat.ACC: (12, 3, 48)
}

slot_to_available_substat = {
    1: [Stat.ATK_P, Stat.HP, Stat.HP_P, Stat.SPD, Stat.CRate, Stat.CDmg, Stat.RES, Stat.ACC],
    2: [Stat.ATK, Stat.ATK_P, Stat.DEF, Stat.DEF_P, Stat.HP, Stat.HP_P, Stat.SPD, Stat.CRate, Stat.CDmg, Stat.RES, Stat.ACC],
    3: [Stat.DEF_P, Stat.HP, Stat.HP_P, Stat.SPD, Stat.CRate, Stat.CDmg, Stat.RES, Stat.ACC],
    4: [Stat.ATK, Stat.ATK_P, Stat.DEF, Stat.DEF_P, Stat.HP, Stat.HP_P, Stat.SPD, Stat.CRate, Stat.CDmg, Stat.RES, Stat.ACC],
    5: [Stat.ATK, Stat.ATK_P, Stat.DEF, Stat.DEF_P, Stat.HP_P, Stat.SPD, Stat.CRate, Stat.CDmg, Stat.RES, Stat.ACC],
    6: [Stat.ATK, Stat.ATK_P, Stat.DEF, Stat.DEF_P, Stat.HP, Stat.HP_P, Stat.SPD, Stat.CRate, Stat.CDmg, Stat.RES, Stat.ACC]
}

slot_to_available_mainstat = {
    1: [Stat.ATK],
    2: [Stat.ATK, Stat.ATK_P, Stat.DEF, Stat.DEF_P, Stat.HP, Stat.HP_P, Stat.SPD],
    3: [Stat.DEF],
    4: [Stat.ATK, Stat.ATK_P, Stat.DEF, Stat.DEF_P, Stat.HP, Stat.HP_P, Stat.CRate, Stat.CDmg],
    5: [Stat.HP],
    6: [Stat.ATK, Stat.ATK_P, Stat.DEF, Stat.DEF_P, Stat.HP, Stat.HP_P, Stat.RES, Stat.ACC]
}
