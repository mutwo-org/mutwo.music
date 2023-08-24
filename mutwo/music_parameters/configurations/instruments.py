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
del (a, w, wi, music_parameters, ranges)
