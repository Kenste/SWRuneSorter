from dsl.dsl import (AND,
                     OR,
                     NOT,
                     AtLeast,
                     Level,
                     Legend,
                     Hero,
                     Stars,
                     Slot,
                     Set,
                     ATK,
                     ATK_P,
                     DEF,
                     DEF_P,
                     HP,
                     HP_P,
                     SPD,
                     CRate,
                     CDmg,
                     RES,
                     ACC,
                     Main,
                     Innate)



# Basically thresholds for Hero runes, as this expects 3 good rolls into one stat.
# Legend runes just get 1 more roll into some random stat.
single_sub_threshold = OR(
    ATK_P >= 30,
    DEF_P >= 30,
    HP_P >= 30,
    ACC >= 32, # Less important than atk, def, hp
    RES >= 32, # Less important than atk, def, hp
    SPD >= 20,
    CRate >= 20,
    CDmg >= 25
)

# Hero runes cannot or should not be able to cover this, as this expects 2 good rolls into 2 different stats.
# This covers Legend runes rolling into 2 stats, which I think is totally fine.
two_subs_thresholds_conditions = [
    ATK_P >= 20,
    DEF_P >= 20,
    HP_P >= 20,
    ACC >= 21,
    RES >= 21,
    SPD >= 15,
    CRate >= 15,
    CDmg >= 17
]
two_subs_thresholds = AtLeast(
    2,
    *two_subs_thresholds_conditions
)

# I currently do not cover 1 upgrade into each stat in either rune rarity, as I don't think this provides much value.
# It would be useful when accounting for the different combinations where it is helpful.
# E.g. Upgrading crit rate, crit dmg, and atk% might be something we want, but certain combinations might be less desired.
# However, there are a lot of combinations, that I don't want to account for at this point.
# I also do not account for Hero runes rolling twice into one stat and once into another for the same reason.
subs = OR(
    single_sub_threshold,
    two_subs_thresholds
)


level_12 = AND(
    Level.InRange(12, 15),
    subs
)