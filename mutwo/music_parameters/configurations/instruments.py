import itertools

import ranges

from mutwo import music_parameters

a, w, wi = (  # abbreviation for more compact code
    music_parameters.OctaveAmbitus,
    music_parameters.WesternPitch,
    music_parameters.WesternPitchInterval,
)

DEFAULT_PICCOLO_DICT = dict(
    name="piccolo",
    short_name="pcl.",
    pitch_ambitus=a(w("d", 5), w("c", 8)),
    pitch_count_range=ranges.Range(1, 2),
    transposition_pitch_interval=wi("p-8"),
)
"""Default arguments for :class:`mutwo.music_parameters.Piccolo`."""

DEFAULT_FLUTE_DICT = dict(
    name="flute",
    short_name="flt.",
    pitch_ambitus=a(w("c", 4), w("d", 7)),
    pitch_count_range=ranges.Range(1, 2),
    transposition_pitch_interval=wi("p1"),
)
"""Default arguments for :class:`mutwo.music_parameters.Flute`."""

DEFAULT_OBOE_DICT = dict(
    name="oboe",
    short_name="ob.",
    pitch_ambitus=a(w("bf", 3), w("a", 6)),
    pitch_count_range=ranges.Range(1, 2),
    transposition_pitch_interval=wi("p1"),
)
"""Default arguments for :class:`mutwo.music_parameters.Oboe`."""

DEFAULT_BF_CLARINET_DICT = dict(
    name="bf-clarinet",
    short_name="bf-cl.",
    pitch_ambitus=a(w("d", 3), w("bf", 6)),
    pitch_count_range=ranges.Range(1, 2),
    transposition_pitch_interval=wi("m2"),
)
"""Default arguments for :class:`mutwo.music_parameters.BfClarinet`."""

DEFAULT_EF_CLARINET_DICT = dict(
    name="ef-clarinet",
    short_name="ef-cl.",
    pitch_ambitus=a(w("g", 3), w("ef", 7)),
    pitch_count_range=ranges.Range(1, 2),
    transposition_pitch_interval=wi("m-3"),
)
"""Default arguments for :class:`mutwo.music_parameters.EfClarinet`."""

DEFAULT_BASSOON_DICT = dict(
    name="bassoon",
    short_name="bs.",
    pitch_ambitus=a(w("bf", 1), w("ef", 5)),
    pitch_count_range=ranges.Range(1, 2),
    transposition_pitch_interval=wi("p1"),
)
"""Default arguments for :class:`mutwo.music_parameters.Bassoon`."""


# ############################################################# #
#   Celtic Harp                                                 #
# ############################################################# #


h = music_parameters.constants.HarpFinger

DEFAULT_STRING_DISTANCE_TO_FINGER_INDEX_PAIR_TUPLE_DICT = {
    # We can't touch far away strings with close fingers. Harps have
    # around 1.6cm string spacing in lower register:
    #   https://heartlandharps.com/string-spacing/
    # Numbers are gained from experiments with my hand + 1.6cm string
    # spacing.
    1: (
        (h.RightTwo, h.RightOne),
        (h.RightThree, h.RightTwo),
        (h.RightFour, h.RightThree),
    ),
    2: (
        (h.RightTwo, h.RightOne),
        (h.RightThree, h.RightOne),
        (h.RightThree, h.RightTwo),
        (h.RightFour, h.RightTwo),
        (h.RightFour, h.RightThree),
    ),
    3: (
        (h.RightTwo, h.RightOne),
        (h.RightThree, h.RightOne),
        (h.RightFour, h.RightOne),
        (h.RightThree, h.RightTwo),
        (h.RightFour, h.RightTwo),
    ),
    4: (
        (h.RightTwo, h.RightOne),
        (h.RightThree, h.RightOne),
        (h.RightFour, h.RightOne),
        (h.RightFour, h.RightTwo),
    ),
    5: (
        (h.RightTwo, h.RightOne),
        (h.RightThree, h.RightOne),
        (h.RightFour, h.RightOne),
        (h.RightFour, h.RightTwo),
    ),
    6: (
        (h.RightTwo, h.RightOne),
        (h.RightThree, h.RightOne),
        (h.RightFour, h.RightOne),
    ),
    7: (
        (h.RightTwo, h.RightOne),
        (h.RightThree, h.RightOne),
        (h.RightFour, h.RightOne),
    ),
    8: ((h.RightThree, h.RightOne), (h.RightFour, h.RightOne)),
    9: ((h.RightFour, h.RightOne),),
}
"""Default value for `string_distance_to_finger_index_pair_tuple_dict`
argument of :class:`mutwo.music_parameters.CelticHarp`."""

# Harp uses 'two left hands' (both hands work in the same way).
for k in DEFAULT_STRING_DISTANCE_TO_FINGER_INDEX_PAIR_TUPLE_DICT:
    DEFAULT_STRING_DISTANCE_TO_FINGER_INDEX_PAIR_TUPLE_DICT[k] += tuple(
        (-a, -b) for a, b in DEFAULT_STRING_DISTANCE_TO_FINGER_INDEX_PAIR_TUPLE_DICT[k]
    )

# Distance doesn't matter if we use two different hands; they
# can be as far as possible.
joker = tuple(
    itertools.product(
        (h.LeftFour, h.LeftThree, h.LeftTwo, h.LeftOne),
        (h.RightFour, h.RightThree, h.RightTwo, h.RightOne),
    )
)

for k in range(100):  # Assume we have max 100 different strings
    try:
        DEFAULT_STRING_DISTANCE_TO_FINGER_INDEX_PAIR_TUPLE_DICT[k] += joker
    except KeyError:
        DEFAULT_STRING_DISTANCE_TO_FINGER_INDEX_PAIR_TUPLE_DICT[k] = joker


MA, SI = 1, 0.85  # One score for best (MAIN), one for second (SIDE).
HARP_DELTA_SCORE_MAPPING = {
    # This table has been gained by reading harp beginners scores.
    # One
    (h.RightOne, h.RightOne): {0: MA, -1: SI * 0.85, 1: SI * 0.85},
    (h.RightOne, h.RightTwo): {1: SI, -1: SI, -2: MA, -3: SI},
    (h.RightOne, h.RightThree): {1: SI, -2: SI, -3: SI, -4: MA, -5: SI, -6: SI},
    (h.RightOne, h.RightFour): {-5: SI, -6: MA, -7: SI},
    # Two
    (h.RightTwo, h.RightOne): {-1: SI, 1: SI, 2: MA, 3: SI},
    (h.RightTwo, h.RightTwo): {-1: SI * 0.85, 0: MA, 1: SI * 0.85},
    (h.RightTwo, h.RightThree): {-1: MA, -2: MA, -3: SI},
    (h.RightTwo, h.RightFour): {-3: SI, -4: MA, -5: MA, -6: SI},
    # Three
    (h.RightThree, h.RightOne): {-1: SI, 1: SI, 2: MA, 3: MA, 4: MA, 5: SI},
    (h.RightThree, h.RightTwo): {1: MA, 2: MA, 3: SI},
    (h.RightThree, h.RightThree): {-1: SI * 0.85, 0: MA, 1: SI * 0.85},
    (h.RightThree, h.RightFour): {-1: MA, -2: MA, -3: SI},
    # Four
    (h.RightFour, h.RightOne): {-1: SI, 5: SI, 6: MA, 7: SI},
    (h.RightFour, h.RightTwo): {4: SI, 5: MA, 6: SI},
    (h.RightFour, h.RightThree): {1: MA, 2: MA, 3: SI},
    (h.RightFour, h.RightFour): {-1: SI * 0.85, 0: MA, 1: SI * 0.85},
}
"""Map finger indexes to string-distance -> score mappings.
This is used in :class:`mutwo.music_parameters.CelticHarp`."""

for k, v in tuple(HARP_DELTA_SCORE_MAPPING.items()):
    fi0, fi1 = k
    HARP_DELTA_SCORE_MAPPING[(-fi0, -fi1)] = dict(v)

DEFAULT_CELTIC_HARP_DICT = dict(
    name="harp",
    short_name="hp.",
    pitch_count_range=ranges.Range(1, 8),
    transposition_pitch_interval=wi("p1"),
    pitch_tuple=music_parameters.Scale(
        w("c", 4),
        music_parameters.RepeatingScaleFamily(
            [wi(i) for i in "p1 M2 M3 p4 p5 M6 M7".split(" ")],
            min_pitch_interval=music_parameters.DirectPitchInterval(-1200 * 2),
            max_pitch_interval=music_parameters.DirectPitchInterval(1200 * 3),
        ),
    ).pitch_tuple,
)
"""Default arguments for :class:`mutwo.music_parameters.CelticHarp`."""

# Cleanup!
del (a, w, wi, h, itertools, music_parameters, ranges, joker, k, MA, SI)
