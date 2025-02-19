import attributes
import stats
from logic import AND, OR, NOT
from runescorer.rune import Rune, RuneStat
from src.runescorer import constants

AND = AND
OR = OR
NOT = NOT

Level = attributes.Level()
Legend = attributes.Quality() == constants.Quality.Legend
Hero = attributes.Quality() == constants.Quality.Hero
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

if __name__ == '__main__':
    rune = Rune(main=RuneStat(constants.Stat.ATK_P, 10), quality=constants.Quality.Legend, set="Test", slot=1, innate=RuneStat(constants.Stat.ATK, 10), subs=[RuneStat(constants.Stat.ATK_P, 10), RuneStat(constants.Stat.SPD, 10), RuneStat(constants.Stat.CRate, 5)], level=4, stars=6)
    rune_no_innate = Rune(main=RuneStat(constants.Stat.ATK_P, 10), quality=constants.Quality.Legend, set="Test", slot=1, innate=None, subs=[RuneStat(constants.Stat.ATK_P, 10), RuneStat(constants.Stat.SPD, 10), RuneStat(constants.Stat.CRate, 5)], level=4, stars=6)


    # main stat
    main_stat_filter_success = Main.ATK_P
    main_stat_filter_fail = Main.SPD

    assert main_stat_filter_success(rune)
    assert not main_stat_filter_fail(rune)


    # innate
    innate_stat_filter_success1 = Innate.ATK == 10
    innate_stat_filter_success2 = Innate.ATK >= 10
    innate_stat_filter_success3 = Innate.ATK <= 10
    innate_stat_filter_fail1 = Innate.ATK < 10
    innate_stat_filter_fail2 = Innate.ATK > 10
    innate_stat_filter_fail3 = Innate.ATK != 10
    innate_stat_filter_fail4 = Innate.ATK == 10

    assert innate_stat_filter_success1(rune)
    assert innate_stat_filter_success2(rune)
    assert innate_stat_filter_success3(rune)
    assert not innate_stat_filter_fail1(rune)
    assert not innate_stat_filter_fail2(rune)
    assert not innate_stat_filter_fail3(rune)
    assert not innate_stat_filter_fail4(rune_no_innate)


    # subs
    subs_stat_filter_success = CRate == 5
    subs_stat_filter_fail1 = CDmg >= 0
    subs_stat_filter_fail2 = CDmg < 0
    subs_stat_filter_fail3 = CRate != 5

    assert subs_stat_filter_success(rune)
    assert not subs_stat_filter_fail1(rune)
    assert not subs_stat_filter_fail2(rune)
    assert not subs_stat_filter_fail3(rune)


    # level
    level_filter_success1 = Level == 4
    level_filter_success2 = Level >= 4
    level_filter_success3 = Level <= 4
    level_filter_fail1 = Level < 4
    level_filter_fail2 = Level > 4
    level_filter_fail3 = Level != 4

    assert level_filter_success1(rune)
    assert level_filter_success2(rune)
    assert level_filter_success3(rune)
    assert not level_filter_fail1(rune)
    assert not level_filter_fail2(rune)
    assert not level_filter_fail3(rune)


    # quality
    quality_filter_success = Legend
    quality_filter_fail = Hero

    assert quality_filter_success(rune)
    assert not quality_filter_fail(rune)


    # stars
    stars_filter_success1 = Stars == 6
    stars_filter_success2 = Stars >= 6
    stars_filter_success3 = Stars <= 6
    stars_filter_success4 = Stars > 5
    stars_filter_success5 = Stars < 7
    stars_filter_fail1 = Stars < 6
    stars_filter_fail2 = Stars > 6
    stars_filter_fail3 = Stars != 6

    assert stars_filter_success1(rune)
    assert stars_filter_success2(rune)
    assert stars_filter_success3(rune)
    assert stars_filter_success4(rune)
    assert stars_filter_success5(rune)
    assert not stars_filter_fail1(rune)
    assert not stars_filter_fail2(rune)
    assert not stars_filter_fail3(rune)


    # slot
    slot_filter_success1 = Slot == 1
    slot_filter_success2 = Slot.In([1, 2])
    slot_filter_fail1 = Slot != 1
    slot_filter_fail2 = Slot == 2
    slot_filter_fail3 = Slot.In([2, 3])

    assert slot_filter_success1(rune)
    assert slot_filter_success2(rune)
    assert not slot_filter_fail1(rune)
    assert not slot_filter_fail2(rune)
    assert not slot_filter_fail3(rune)


    # set
    set_filter_success1 = Set == "Test"
    set_filter_success2 = Set.In(["Test", "Rage"])
    set_filter_fail1 = Set == "Rage"
    set_filter_fail2 = Set.In(["Rage"])

    assert set_filter_success1(rune)
    assert set_filter_success2(rune)
    assert not set_filter_fail1(rune)
    assert not set_filter_fail2(rune)


    # combination
    some_main_filter = OR(Main.HP_P, Main.ATK_P)
    some_innate_filter = Innate.ATK >= 5
    some_subs_filter = AND(SPD > 4, ATK_P <= 10, ATK_P > 9)
    some_level_filter = AND(Level >= 4, Level < 5)
    dsl_filter_success = AND(some_main_filter, some_innate_filter, some_subs_filter, some_level_filter)

    assert dsl_filter_success(rune)
