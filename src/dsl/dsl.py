import stats
from src.runescorer import constants

ATK = stats.ATK()
ATK_P = stats.ATK_P()
DEF = stats.DEF()
DEF_P = stats.DEF_P()
HP = stats.HP()
HP_P = stats.HP_P()
SPD = stats.SPD()
CRate = stats.CRate()
CDmg = stats.CDmg()
RES = stats.RES()
ACC = stats.ACC()


class Main:
    ATK = stats.ATK(constants.StatLocation.Main) == constants.Stat.ATK
    ATK_P = stats.ATK_P(constants.StatLocation.Main) == constants.Stat.ATK_P
    DEF = stats.DEF(constants.StatLocation.Main) == constants.Stat.DEF
    DEF_P = stats.DEF_P(constants.StatLocation.Main) == constants.Stat.DEF_P
    HP = stats.HP(constants.StatLocation.Main) == constants.Stat.HP
    HP_P = stats.HP_P(constants.StatLocation.Main) == constants.Stat.HP_P
    SPD = stats.SPD(constants.StatLocation.Main) == constants.Stat.SPD
    CRate = stats.CRate(constants.StatLocation.Main) == constants.Stat.CRate
    CDmg = stats.CDmg(constants.StatLocation.Main) == constants.Stat.CDmg
    RES = stats.RES(constants.StatLocation.Main) == constants.Stat.RES
    ACC = stats.ACC(constants.StatLocation.Main) == constants.Stat.ACC


class Innate:
    ATK = stats.ATK(constants.StatLocation.Innate) == constants.Stat.ATK
    ATK_P = stats.ATK_P(constants.StatLocation.Innate) == constants.Stat.ATK_P
    DEF = stats.DEF(constants.StatLocation.Innate) == constants.Stat.DEF
    DEF_P = stats.DEF_P(constants.StatLocation.Innate) == constants.Stat.DEF_P
    HP = stats.HP(constants.StatLocation.Innate) == constants.Stat.HP
    HP_P = stats.HP_P(constants.StatLocation.Innate) == constants.Stat.HP_P
    SPD = stats.SPD(constants.StatLocation.Innate) == constants.Stat.SPD
    CRate = stats.CRate(constants.StatLocation.Innate) == constants.Stat.CRate
    CDmg = stats.CDmg(constants.StatLocation.Innate) == constants.Stat.CDmg
    RES = stats.RES(constants.StatLocation.Innate) == constants.Stat.RES
    ACC = stats.ACC(constants.StatLocation.Innate) == constants.Stat.ACC
