try:
    import quicktions as fractions  # type: ignore
except ImportError:
    import fractions  # type: ignore

# The next import is an exception / a hack!
# Normally this should be:
#   from mutwo import music_parameters; music_parameters.commas...
# But in this case we would get a circular import, therefore
# we have to use this hacky solution.

from . import commas


# ###################################################################### #
#                            configure pitches                           #
# ###################################################################### #

DEFAULT_CONCERT_PITCH = 440
"""The default concert pitch in frequency."""

DEFAULT_CONCERT_PITCH_OCTAVE_FOR_WESTERN_PITCH = 4
"""The default value of ``concert_pitch_octave_for_western_pitch`` for
the `WesternPitch` class. It sets octave of default concert pitch for
western pitch to one line (') (so that the resulting concert pitch is
a' or in midi nomenclature a4)"""

DEFAULT_CONCERT_PITCH_PITCH_CLASS_FOR_WESTERN_PITCH = 9
"""The default value of``concert_pitch_concert_pitch_class_for_western_pitch``
for the `WesternPitch` class. It sets pitch class 'a' as the default pitch class
for the concert pitch of the WesternPitch class."""

ACCIDENTAL_NAME_TO_PITCH_CLASS_MODIFICATION_DICT = {
    # multiply with 2 because the difference of "1" in pitch
    # class is defined as one chromatic step (see class
    # definition of WesternPitch)
    accidental_name: accidental_value * 2
    for accidental_name, accidental_value in {
        # double sharp / double flat
        "ff": -fractions.Fraction(1, 1),
        "ss": fractions.Fraction(1, 1),
        # eleven twelfth-tone
        "etf": -fractions.Fraction(11, 12),
        "ets": fractions.Fraction(11, 12),
        # seven eigth-tone
        "sef": -fractions.Fraction(7, 8),
        "ses": fractions.Fraction(7, 8),
        # two third-tone
        "trf": -fractions.Fraction(2, 3),
        "trs": fractions.Fraction(2, 3),
        # three quarter-tone
        "tqf": -fractions.Fraction(3, 4),
        "tqs": fractions.Fraction(3, 4),
        # seven sixth-tone
        "sxf": -fractions.Fraction(7, 6),
        "sxs": fractions.Fraction(7, 6),
        # nine eight-tone
        "nef": -fractions.Fraction(9, 8),
        "nes": fractions.Fraction(9, 8),
        # seven twelfth-tone
        "stf": -fractions.Fraction(7, 12),
        "sts": fractions.Fraction(7, 12),
        # ordinary sharp / flat
        "f": -fractions.Fraction(1, 2),
        "s": fractions.Fraction(1, 2),
        # five twelfth-tone
        "ftf": -fractions.Fraction(5, 12),
        "fts": fractions.Fraction(5, 12),
        # three eigth-tone
        "tef": -fractions.Fraction(3, 8),
        "tes": fractions.Fraction(3, 8),
        # one third-tone (use "r" to avoid conufsion with twelfth-tone)
        "rf": -fractions.Fraction(1, 3),
        "rs": fractions.Fraction(1, 3),
        # one quarter-tone
        "qf": -fractions.Fraction(1, 4),
        "qs": fractions.Fraction(1, 4),
        # one sixth-tone (use x to avoid confusion with double-sharp ss)
        "xf": -fractions.Fraction(1, 6),
        "xs": fractions.Fraction(1, 6),
        # one eigth-tone
        "ef": -fractions.Fraction(1, 8),
        "es": fractions.Fraction(1, 8),
        # one twelfth-tone
        "tf": -fractions.Fraction(1, 12),
        "ts": fractions.Fraction(1, 12),
        # no accidental / empty string
        "": fractions.Fraction(0, 1),
    }.items()
}
"""Mapping of accidental name to pitch class modification for the
`WesternPitch` class. When adding new accidentals or changing
accidental names only this constant has to be changed."""

PITCH_CLASS_MODIFICATION_TO_ACCIDENTAL_NAME_DICT = {
    accidental_value: accidental_name
    for accidental_name, accidental_value in ACCIDENTAL_NAME_TO_PITCH_CLASS_MODIFICATION_DICT.items()
}
"""Mapping of pitch class modifications name accidental name for the
`WesternPitch` class. This global variable is defined in reference to
``ACCIDENTAL_NAME_TO_PITCH_CLASS_MODIFICATION``."""

# Tuning commas are organised, so that the relevant prime number
# is always in the numerator of the ratio!
DEFAULT_PRIME_TO_COMMA_DICT = {
    # syntonic comma
    5: commas.Comma(fractions.Fraction(80, 81)),
    # septimal comma
    7: commas.Comma(fractions.Fraction(63, 64)),
    # undecimal quartertone
    11: commas.Comma(fractions.Fraction(33, 32)),
    # tridecimal thirdtone
    13: commas.Comma(fractions.Fraction(26, 27)),
    # 17-limit schisma
    17: commas.Comma(fractions.Fraction(2176, 2187)),
    # 19-limit schisma
    19: commas.Comma(fractions.Fraction(513, 512)),
    # 23-limit comma
    23: commas.Comma(fractions.Fraction(736, 729)),
    # 29-limit sixthtone
    29: commas.Comma(fractions.Fraction(261, 256)),
    # 31-limit quartertone
    31: commas.Comma(fractions.Fraction(31, 32)),
    # 37-limit quartertone
    37: commas.Comma(fractions.Fraction(37, 36)),
    # 41-limit comma
    41: commas.Comma(fractions.Fraction(82, 81)),
    # 43-limit comma
    43: commas.Comma(fractions.Fraction(129, 128)),
    # 47-limit quartertone
    47: commas.Comma(fractions.Fraction(752, 729)),
}
"""Standard commas defined by the `Helmholtz-Ellis JI Pitch Notation <https://marsbat.space/pdfs/notation.pdf>`_."""

DEFAULT_PITCH_ENVELOPE_PARAMETER_NAME = "pitch"
"""Default property parameter name for events in
:class:`mutwo.music_parameters.abc.Pitch.PitchEnvelope`."""

DEFAULT_PITCH_INTERVAL_ENVELOPE_PARAMETER_NAME = "pitch_interval"
"""Default property parameter name for events in
:class:`mutwo.music_parameters.Pitch.PitchIntervalEnvelope`."""

# ###################################################################### #
#                            configure volumes                           #
# ###################################################################### #

DEFAULT_MINIMUM_DECIBEL_FOR_MIDI_VELOCITY_AND_STANDARD_DYNAMIC_INDICATOR: float = -40
"""Default value for ``minimum_decibel`` in
:class:`~mutwo.music_parameters.WesternVolume` and in
:method:`~mutwo.music_parameters.abc.Volume.decibel_to_midi_velocity`."""

DEFAULT_MAXIMUM_DECIBEL_FOR_MIDI_VELOCITY_AND_STANDARD_DYNAMIC_INDICATOR: float = 0
"""Default value for ``maximum_decibel`` in
:class:`~mutwo.music_parameters.WesternVolume` and in
:method:`~mutwo.music_parameters.abc.Volume.decibel_to_midi_velocity`."""

# ###################################################################### #
#                            configure lyrics                            #
# ###################################################################### #

DEFAULT_LANGUAGE_CODE = "mb-en1"
"""The default language code for
:class:`mutwo.music_parameters.LanguageBasedLyric`. This has to be supported
by the mbrola backend. To get a list of all supported language codes
you can run:

>>> import phonemizer
>>> phonemizer.backend.EspeakMbrolaBackend._all_supported_languages()
"""


# ###################################################################### #
# ###################################################################### #
# ###################################################################### #
# Cleanup module
del commas, fractions
