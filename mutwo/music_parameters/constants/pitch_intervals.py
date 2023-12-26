import enum


class WesternPitchIntervalQuality(str, enum.Enum):
    """Define interval qualities according to Western music theory."""

    PERFECT = "perfect"
    MINOR = "minor"
    MAJOR = "major"
    AUGMENTED = "augmented"
    DIMINISHED = "diminished"


class WesternPitchIntervalType(str, enum.Enum):
    """Define interval types according to Western music theory."""

    PRIME = "1"
    SECOND = "2"
    THIRD = "3"
    FOURTH = "4"
    FIFTH = "5"
    SIXTH = "6"
    SEVENTH = "7"


WESTERN_PITCH_INTERVAL_QUALITY_TO_CENT_DEVIATION_DICT = {
    WesternPitchIntervalQuality.PERFECT: 0,
    WesternPitchIntervalQuality.MINOR: -100,
    WesternPitchIntervalQuality.MAJOR: 0,
    WesternPitchIntervalQuality.DIMINISHED: -100,
    WesternPitchIntervalQuality.AUGMENTED: 100,
}
"""Set relationship between pitch interval quality
and cent deviation."""

WESTERN_PITCH_INTERVAL_BASE_TYPE_TO_CENT_DEVIATION_DICT = {
    WesternPitchIntervalType.PRIME: 0,
    WesternPitchIntervalType.SECOND: 200,
    WesternPitchIntervalType.THIRD: 400,
    WesternPitchIntervalType.FOURTH: 500,
    WesternPitchIntervalType.FIFTH: 700,
    WesternPitchIntervalType.SIXTH: 900,
    WesternPitchIntervalType.SEVENTH: 1100,
}
"""Set relationship between pitch interval type
and cent position."""

SEMITONE_TO_WESTERN_PITCH_INTERVAL_BASE_TYPE_AND_QUALITY_DICT = {
    0: (WesternPitchIntervalType.PRIME, WesternPitchIntervalQuality.PERFECT),
    1: (WesternPitchIntervalType.SECOND, WesternPitchIntervalQuality.MINOR),
    2: (WesternPitchIntervalType.SECOND, WesternPitchIntervalQuality.MAJOR),
    3: (WesternPitchIntervalType.THIRD, WesternPitchIntervalQuality.MINOR),
    4: (WesternPitchIntervalType.THIRD, WesternPitchIntervalQuality.MAJOR),
    5: (WesternPitchIntervalType.FOURTH, WesternPitchIntervalQuality.PERFECT),
    # Yes, the next entry is arbitary and could also be:
    # (WesternPitchIntervalType.FIFTH, WesternPitchIntervalQuality.DIMINISHED)
    6: (WesternPitchIntervalType.FOURTH, WesternPitchIntervalQuality.AUGMENTED),
    7: (WesternPitchIntervalType.FIFTH, WesternPitchIntervalQuality.PERFECT),
    8: (WesternPitchIntervalType.SIXTH, WesternPitchIntervalQuality.MINOR),
    9: (WesternPitchIntervalType.SIXTH, WesternPitchIntervalQuality.MAJOR),
    10: (WesternPitchIntervalType.SEVENTH, WesternPitchIntervalQuality.MINOR),
    11: (WesternPitchIntervalType.SEVENTH, WesternPitchIntervalQuality.MAJOR),
}
"""This dictionary maps 12 semitones (from prime to major seventh) to
a default western pitch interval type and related western pitch interval
quality. This dictionary is used in the conversion from semitones to
western pitch interval instances."""

WESTERN_PITCH_INTERVAL_BASE_TYPE_COUNT = len(
    WESTERN_PITCH_INTERVAL_BASE_TYPE_TO_CENT_DEVIATION_DICT
)
"""How many western pitch base intervals exist"""

PERFECT_INTERVAL_TYPE_TUPLE = (
    WesternPitchIntervalType.PRIME,
    WesternPitchIntervalType.FOURTH,
    WesternPitchIntervalType.FIFTH,
)
"""A tuple with names of all perfect intervals
(e.g. intervals which know the 'perfect', the
'augmented' and the 'diminished' qualities)"""

IMPERFECT_INTERVAL_TYPE_TUPLE = (
    WesternPitchIntervalType.SECOND,
    WesternPitchIntervalType.THIRD,
    WesternPitchIntervalType.SIXTH,
    WesternPitchIntervalType.SEVENTH,
)
"""A tuple with names of all imperfect intervals
(e.g. intervals which know the 'major', the 'minor',
the 'augmented' and the 'diminished' qualities)"""

ALLOWED_WESTERN_PITCH_INTERVAL_QUALITY_FOR_PERFECT_INTERVAL_TUPLE = (
    WesternPitchIntervalQuality.PERFECT,
    WesternPitchIntervalQuality.AUGMENTED,
    WesternPitchIntervalQuality.DIMINISHED,
)
"""A tuple which lists all names of perfect intervals
(e.g. intervals which know the 'perfect', the
'augmented' and the 'diminished' qualities)"""

ALLOWED_WESTERN_PITCH_INTERVAL_QUALITY_FOR_IMPERFECT_INTERVAL_TUPLE = (
    WesternPitchIntervalQuality.MINOR,
    WesternPitchIntervalQuality.MAJOR,
    WesternPitchIntervalQuality.AUGMENTED,
    WesternPitchIntervalQuality.DIMINISHED,
)
"""A tuple which lists all names of imperfect intervals
(e.g. intervals which know the 'major', the 'minor',
the 'augmented' and the 'diminished' qualities)"""

STACKABLE_WESTERN_PITCH_INTERVAL_QUALITY_TUPLE = (
    WesternPitchIntervalQuality.AUGMENTED,
    WesternPitchIntervalQuality.DIMINISHED,
)
"""A tuple which lists all interval qualities which
can be stacked (e.g. added multiple times to an
interval type."""

del enum
