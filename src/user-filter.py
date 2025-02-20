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

# Modify the filtering of stats and attributes of a rune to your needs.
# The `rune_filter` has to stay and will be used as the final filter.
# You can define more variables e.g. to define runes of a specific level and merge them at the end in the `rune_filer`:
#
# rune_level_0 = AND(Level == 0, ...)
# rune_level_3 = AND(Level == 3, ...)
# rune_level_12 = AND(Level == 12, ...)
# rune_filter = OR(rune_level_0, rune_level_3, rune_level_12)
#
# Note though, that level is an interesting attribute:
# *Currently* if you would use the example, and a rune is on level 9, it would not pass the filter, i.e. sold,
# simply because there is no filter for Level 9, or a "catch-all" alternative, where no Level is defined.
# Instead, to not encounter any issues, use `Level.InRange`, to avoid any issues when following this approach. i.e.:
#
# rune_level_0 = AND(Level.InRange(0, 2), ...)
# rune_level_3 = AND(Level.InRange(3,11), ...)
# rune_level_12 = AND(Level.InRange(12, 15), ...)
# rune_filter = OR(rune_level_0, rune_level_3, rune_level_12)
#
# This way any rune with Level 3 to 11 is checked against the `rune_level_3` filter.
# This avoids selling potentially good runes, for which you did not define a filter.

rune_filter = SPD >= 0

