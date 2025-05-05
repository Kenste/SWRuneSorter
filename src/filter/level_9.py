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
from filter.level_12 import single_sub_threshold, two_subs_thresholds_conditions

# Legend rune that has upgrades one stat twice, so theoretically upgrading two different stats twice is possible.
potential_legend = AND(
    Legend,
    OR(
        *two_subs_thresholds_conditions
    )
)

# Check if we already achieved the threshold of a single stat.
done_hero = single_sub_threshold


subs = OR(
    potential_legend,
    done_hero
)

# Level 9 serves as a bridge to checking if we have an "optimal" rune.
# It's mostly useful to reduce the loss of money by upgrading a "bad" rune.
# So we essentially need to make sure that all the target stats defined for level 12 are achievable at this point.
level_9 = AND(
    Level.InRange(9, 11),
    subs
)