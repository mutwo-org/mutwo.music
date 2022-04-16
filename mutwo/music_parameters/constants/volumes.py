MINIMUM_VELOCITY = 0
"""the lowest allowed midi velocity value"""

MAXIMUM_VELOCITY = 127
"""the highest allowed midi velocity value"""

# standard volume indicator
STANDARD_DYNAMIC_INDICATOR = tuple(
    "ppppp pppp ppp pp p mp mf f ff fff ffff fffff".split(" ")
)
"""Standard European music dynamic indicator"""

SPECIAL_DYNAMIC_INDICATOR_TO_STANDARD_DYNAMIC_INDICATOR_DICT = {
    "fp": "mf",
    "sf": "f",
    "sff": "ff",
    "sfz": "ff",
    "sp": "p",
    "spp": "pp",
    "rfz": "f",
}
"""European music indicator with special meaning.

For the sake of simplicity they have been mapped to standard dynamic
indicator (for having the same amplitude)."""

DYNAMIC_INDICATOR_TUPLE = STANDARD_DYNAMIC_INDICATOR + tuple(
    SPECIAL_DYNAMIC_INDICATOR_TO_STANDARD_DYNAMIC_INDICATOR_DICT.keys()
)
"""all available dynamic indicator for :class:`WesternVolume`"""
