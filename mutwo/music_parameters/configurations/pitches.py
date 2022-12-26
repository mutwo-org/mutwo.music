try:
    import quicktions as fractions  # type: ignore
except ImportError:
    import fractions  # type: ignore

# The next import is an exception / a hack!
# Normally this should be:
#   from mutwo import music_parameters; music_parameters.commas...
# But in this case we would get a circular import, therefore
# we have to use this hacky solution.
from .. import commas

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

EQUAL_DIVIDED_OCTAVE_PITCH_ROUND_FREQUENCY_DIGIT_COUNT = 4
"""By how many digits `frequency` of :class:`mutwo.music_parameters.EqualDividedOctavePitch`
is rounded. This helps fixing floating point errors."""

del commas, fractions
