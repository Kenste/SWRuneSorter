import attributes
import stats
from src.runescorer import constants

Level = attributes.Level()
Legend = attributes.Quality(constants.Quality.Legend)
Hero = attributes.Quality(constants.Quality.Hero)
Stars = attributes.Stars()
Slot = attributes.Slot()
Set = attributes.Set()

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
    ATK = stats.ATK(constants.StatLocation.Main) == 0
    ATK_P = stats.ATK_P(constants.StatLocation.Main) == 0
    DEF = stats.DEF(constants.StatLocation.Main) == 0
    DEF_P = stats.DEF_P(constants.StatLocation.Main) == 0
    HP = stats.HP(constants.StatLocation.Main) == 0
    HP_P = stats.HP_P(constants.StatLocation.Main) == 0
    SPD = stats.SPD(constants.StatLocation.Main) == 0
    CRate = stats.CRate(constants.StatLocation.Main) == 0
    CDmg = stats.CDmg(constants.StatLocation.Main) == 0
    RES = stats.RES(constants.StatLocation.Main) == 0
    ACC = stats.ACC(constants.StatLocation.Main) == 0


class Innate:
    ATK = stats.ATK(constants.StatLocation.Innate)
    ATK_P = stats.ATK_P(constants.StatLocation.Innate)
    DEF = stats.DEF(constants.StatLocation.Innate)
    DEF_P = stats.DEF_P(constants.StatLocation.Innate)
    HP = stats.HP(constants.StatLocation.Innate)
    HP_P = stats.HP_P(constants.StatLocation.Innate)
    SPD = stats.SPD(constants.StatLocation.Innate)
    CRate = stats.CRate(constants.StatLocation.Innate)
    CDmg = stats.CDmg(constants.StatLocation.Innate)
    RES = stats.RES(constants.StatLocation.Innate)
    ACC = stats.ACC(constants.StatLocation.Innate)
