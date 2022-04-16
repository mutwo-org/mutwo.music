WESTERN_PITCH_INTERVAL_QUALITY_PERFECT = "perfect"
"""Variable to defines an interval with a 'perfect'
quality in terms of Western music theory."""

WESTERN_PITCH_INTERVAL_QUALITY_MINOR = "minor"
"""Variable to defines an interval with a 'minor'
quality in terms of Western music theory."""

WESTERN_PITCH_INTERVAL_QUALITY_MAJOR = "major"
"""Variable to defines an interval with a 'major'
quality in terms of Western music theory."""

WESTERN_PITCH_INTERVAL_QUALITY_AUGMENTED = "augmented"
"""Variable to defines an interval with a 'augmented'
quality in terms of Western music theory."""

WESTERN_PITCH_INTERVAL_QUALITY_DIMINISHED = "diminished"
"""Variable to defines an interval with a 'diminished'
quality in terms of Western music theory."""

WESTERN_PITCH_INTERVAL_TYPE_PRIME = "1"
"""Variable to define an interval between two equal
pitches in European nomenclature."""

WESTERN_PITCH_INTERVAL_TYPE_SECOND = "2"
"""Variable to define an interval between two
pitches with a distance of a step in European
nomenclature."""

WESTERN_PITCH_INTERVAL_TYPE_THIRD = "3"
"""Variable to define an interval between two
pitches with a distance of a third in European
nomenclature."""

WESTERN_PITCH_INTERVAL_TYPE_FOURTH = "4"
"""Variable to define an interval between two
pitches with a distance of a fourth in European
nomenclature."""

WESTERN_PITCH_INTERVAL_TYPE_FIFTH = "5"
"""Variable to define an interval between two
pitches with a distance of a fifth in European
nomenclature."""

WESTERN_PITCH_INTERVAL_TYPE_SIXTH = "6"
"""Variable to define an interval between two
pitches with a distance of a sixth in European
nomenclature."""

WESTERN_PITCH_INTERVAL_TYPE_SEVENTH = "7"
"""Variable to define an interval between two
pitches with a distance of a seventh in European
nomenclature."""

WESTERN_PITCH_INTERVAL_QUALITY_TO_CENT_DEVIATION_DICT = {
    WESTERN_PITCH_INTERVAL_QUALITY_PERFECT: 0,
    WESTERN_PITCH_INTERVAL_QUALITY_MINOR: -100,
    WESTERN_PITCH_INTERVAL_QUALITY_MAJOR: 0,
    WESTERN_PITCH_INTERVAL_QUALITY_DIMINISHED: -100,
    WESTERN_PITCH_INTERVAL_QUALITY_AUGMENTED: 100,
}
"""Set relationship between pitch interval quality
and cent deviation."""

WESTERN_PITCH_INTERVAL_BASE_TYPE_TO_CENT_DEVIATION_DICT = {
    WESTERN_PITCH_INTERVAL_TYPE_PRIME: 0,
    WESTERN_PITCH_INTERVAL_TYPE_SECOND: 200,
    WESTERN_PITCH_INTERVAL_TYPE_THIRD: 400,
    WESTERN_PITCH_INTERVAL_TYPE_FOURTH: 500,
    WESTERN_PITCH_INTERVAL_TYPE_FIFTH: 700,
    WESTERN_PITCH_INTERVAL_TYPE_SIXTH: 900,
    WESTERN_PITCH_INTERVAL_TYPE_SEVENTH: 1100,
}
"""Set relationship between pitch interval type
and cent position."""

SEMITONE_TO_WESTERN_PITCH_INTERVAL_BASE_TYPE_AND_QUALITY_DICT = {
    0: (WESTERN_PITCH_INTERVAL_TYPE_PRIME, WESTERN_PITCH_INTERVAL_QUALITY_PERFECT),
    1: (WESTERN_PITCH_INTERVAL_TYPE_SECOND, WESTERN_PITCH_INTERVAL_QUALITY_MINOR),
    2: (WESTERN_PITCH_INTERVAL_TYPE_SECOND, WESTERN_PITCH_INTERVAL_QUALITY_MAJOR),
    3: (WESTERN_PITCH_INTERVAL_TYPE_THIRD, WESTERN_PITCH_INTERVAL_QUALITY_MINOR),
    4: (WESTERN_PITCH_INTERVAL_TYPE_THIRD, WESTERN_PITCH_INTERVAL_QUALITY_MAJOR),
    5: (WESTERN_PITCH_INTERVAL_TYPE_FOURTH, WESTERN_PITCH_INTERVAL_QUALITY_PERFECT),
    # Yes, the next entry is arbitary and could also be:
    # (WESTERN_PITCH_INTERVAL_TYPE_FIFTH, WESTERN_PITCH_INTERVAL_QUALITY_DIMINISHED)
    6: (WESTERN_PITCH_INTERVAL_TYPE_FOURTH, WESTERN_PITCH_INTERVAL_QUALITY_AUGMENTED),
    7: (WESTERN_PITCH_INTERVAL_TYPE_FIFTH, WESTERN_PITCH_INTERVAL_QUALITY_PERFECT),
    8: (WESTERN_PITCH_INTERVAL_TYPE_SIXTH, WESTERN_PITCH_INTERVAL_QUALITY_MINOR),
    9: (WESTERN_PITCH_INTERVAL_TYPE_SIXTH, WESTERN_PITCH_INTERVAL_QUALITY_MAJOR),
    10: (WESTERN_PITCH_INTERVAL_TYPE_SEVENTH, WESTERN_PITCH_INTERVAL_QUALITY_MINOR),
    11: (WESTERN_PITCH_INTERVAL_TYPE_SEVENTH, WESTERN_PITCH_INTERVAL_QUALITY_MAJOR),
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
    WESTERN_PITCH_INTERVAL_TYPE_PRIME,
    WESTERN_PITCH_INTERVAL_TYPE_FOURTH,
    WESTERN_PITCH_INTERVAL_TYPE_FIFTH,
)
"""A tuple with names of all perfect intervals
(e.g. intervals which know the 'perfect', the
'augmented' and the 'diminished' qualities)"""

IMPERFECT_INTERVAL_TYPE_TUPLE = (
    WESTERN_PITCH_INTERVAL_TYPE_SECOND,
    WESTERN_PITCH_INTERVAL_TYPE_THIRD,
    WESTERN_PITCH_INTERVAL_TYPE_SIXTH,
    WESTERN_PITCH_INTERVAL_TYPE_SEVENTH,
)
"""A tuple with names of all imperfect intervals
(e.g. intervals which know the 'major', the 'minor',
the 'augmented' and the 'diminished' qualities)"""

ALLOWED_WESTERN_PITCH_INTERVAL_QUALITY_FOR_PERFECT_INTERVAL_TUPLE = (
    WESTERN_PITCH_INTERVAL_QUALITY_PERFECT,
    WESTERN_PITCH_INTERVAL_QUALITY_AUGMENTED,
    WESTERN_PITCH_INTERVAL_QUALITY_DIMINISHED,
)
"""A tuple which lists all names of perfect intervals
(e.g. intervals which know the 'perfect', the
'augmented' and the 'diminished' qualities)"""

ALLOWED_WESTERN_PITCH_INTERVAL_QUALITY_FOR_IMPERFECT_INTERVAL_TUPLE = (
    WESTERN_PITCH_INTERVAL_QUALITY_MINOR,
    WESTERN_PITCH_INTERVAL_QUALITY_MAJOR,
    WESTERN_PITCH_INTERVAL_QUALITY_AUGMENTED,
    WESTERN_PITCH_INTERVAL_QUALITY_DIMINISHED,
)
"""A tuple which lists all names of imperfect intervals
(e.g. intervals which know the 'major', the 'minor',
the 'augmented' and the 'diminished' qualities)"""

STACKABLE_WESTERN_PITCH_INTERVAL_QUALITY_TUPLE = (
    WESTERN_PITCH_INTERVAL_QUALITY_AUGMENTED,
    WESTERN_PITCH_INTERVAL_QUALITY_DIMINISHED,
)
"""A tuple which lists all interval qualities which
can be stacked (e.g. added multiple times to an
interval type."""
