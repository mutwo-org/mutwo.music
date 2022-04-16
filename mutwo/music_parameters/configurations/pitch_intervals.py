from mutwo import music_parameters

WESTERN_PITCH_INTERVAL_QUALITY_NAME_TO_ABBREVIATION_DICT = {
    music_parameters.constants.WESTERN_PITCH_INTERVAL_QUALITY_PERFECT: "p",
    music_parameters.constants.WESTERN_PITCH_INTERVAL_QUALITY_MINOR: "m",
    music_parameters.constants.WESTERN_PITCH_INTERVAL_QUALITY_MAJOR: "M",
    music_parameters.constants.WESTERN_PITCH_INTERVAL_QUALITY_AUGMENTED: "A",
    music_parameters.constants.WESTERN_PITCH_INTERVAL_QUALITY_DIMINISHED: "d",
}
"""Maps the quality of a pitch interval to its short
name. The short name is used in the initialisation of
:class:`mutwo.music_parameters.WesternPitchInterval`.
The default names are inspired by the names used in
the python library `music21 <http://web.mit.edu/music21/>`_.
The shorts names can be changed by the user. The keys shouldn't
be changed."""

FALLING_WESTERN_PITCH_INTERVAL_INDICATOR = "-"
"""String to indicate that an interval is falling.
The default value is inspired by the value used in
the python library `music21 <http://web.mit.edu/music21/>`_."""

# Cleanup
del music_parameters
