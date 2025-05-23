from dsl import attributes, operators, stats
from runescorer import constants
from runescorer.rune import Rune, RuneStat

AND = operators.AND
OR = operators.OR
NOT = operators.NOT
AtLeast = operators.AtLeast

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
    level_filter_success4 = Level.InRange(1, 12)
    level_filter_success5 = Level.InRange(4, 12)
    level_filter_success6 = Level.InRange(1, 4)
    level_filter_fail1 = Level < 4
    level_filter_fail2 = Level > 4
    level_filter_fail3 = Level != 4
    level_filter_fail4 = Level.InRange(1, 3)
    level_filter_fail5 = Level.InRange(5, 12)

    assert level_filter_success1(rune)
    assert level_filter_success2(rune)
    assert level_filter_success3(rune)
    assert level_filter_success4(rune)
    assert level_filter_success5(rune)
    assert level_filter_success6(rune)
    assert not level_filter_fail1(rune)
    assert not level_filter_fail2(rune)
    assert not level_filter_fail3(rune)
    assert not level_filter_fail4(rune)
    assert not level_filter_fail5(rune)


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

    # operators
    ## and
    func1_called = False
    func2_called = False
    def test_func1(_):
        global func1_called
        func1_called = True
        return False
    def test_func2(_):
        global func2_called
        func2_called = True
        return True
    and_fail = AND(
        test_func1,
        test_func2,
    )
    and_success = AND(
        lambda _: True,
        lambda _: True,
        lambda _: True
    )
    assert and_success(rune)
    assert not and_fail(rune)
    # short-circuit
    assert func1_called
    assert not func2_called

    ## or
    func1_called = False
    func2_called = False
    or_success = OR(
        test_func2,
        test_func1,
    )
    or_fail = OR(
        lambda _: False,
        lambda _: False,
        lambda _: False
    )
    assert or_success(rune)
    assert not or_fail(rune)
    # short-circuit
    assert func2_called
    assert not func1_called

    ## not
    assert NOT(lambda _: False)(rune)
    assert not NOT(lambda _: True)(rune)

    ## atleast
    func1_called = False
    func2_called = False
    func3_called = False
    func4_called = False
    func5_called = False
    def test_func3(_):
        global func3_called
        func3_called = True
        return True
    def test_func4(_):
        global func4_called
        func4_called = True
        return True
    def test_func5(_):
        global func5_called
        func5_called = True
        return True

    atleast_success = AtLeast(3,
                              test_func1,
                              test_func2,
                              test_func3,
                              test_func4,
                              test_func5,
                              )
    atleast_fail = AtLeast(5,
                              test_func1,
                              test_func2,
                              test_func3,
                              test_func4,
                              test_func5,
                              )
    assert atleast_success(rune)
    # short-circuit
    assert func1_called
    assert func2_called
    assert func3_called
    assert func4_called
    assert not func5_called
    assert not atleast_fail(rune)


    # combination
    some_main_filter = OR(Main.HP_P, Main.ATK_P)
    some_innate_filter = Innate.ATK >= 5
    some_subs_filter = AND(SPD > 4, ATK_P <= 10, ATK_P > 9)
    some_level_filter = AND(Level >= 4, Level < 5)
    some_stars_filter = NOT(Stars < 6)

    dsl_filter_success = AND(
        some_main_filter,
        some_innate_filter,
        some_subs_filter,
        some_level_filter,
        some_stars_filter
    )

    assert dsl_filter_success(rune)
    assert not AND(dsl_filter_success, ACC > 1000)(rune)
