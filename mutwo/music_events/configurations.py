"""Set default values for :class:`mutwo.music_events.NoteLike`."""

import fractions
import numbers
import typing

import quicktions

from mutwo import core_events
from mutwo import music_parameters

DEFAULT_PLAYING_INDICATORS_COLLECTION_CLASS = (
    music_parameters.PlayingIndicatorCollection
)
"""Default value for :attr:`mutwo.music_events.NoteLike.playing_indicator_collection`
in :class:`~mutwo.music_events.NoteLike`"""

DEFAULT_NOTATION_INDICATORS_COLLECTION_CLASS = (
    music_parameters.NotationIndicatorCollection
)
"""Default value for :attr:`mutwo.music_events.NoteLike.notation_indicator_collection`
in :class:`~mutwo.music_events.NoteLike`"""


def _unknown_object_to_pitch_list(
    unknown_object: typing.Any,
) -> list[music_parameters.abc.Pitch]:
    match unknown_object:
        case None:
            pitch_list = []
        case music_parameters.abc.Pitch():
            pitch_list = [unknown_object]
        case str():
            pitch_list = [
                _string_to_pitch(pitch_indication)
                for pitch_indication in unknown_object.split(" ")
            ]
        case fractions.Fraction() | quicktions.Fraction():
            pitch_list = [music_parameters.JustIntonationPitch(unknown_object)]
        case float() | int():
            pitch_list = [music_parameters.WesternPitch(unknown_object)]
        case _:
            raise NotImplementedError(
                f"Can't build pitch object from object '{unknown_object}' "
                f"of type '{type(unknown_object)}'."
            )

    return pitch_list


def _string_to_pitch(pitch_indication: str) -> music_parameters.abc.Pitch:
    # assumes it is a ratio
    if "/" in pitch_indication:
        return music_parameters.JustIntonationPitch(pitch_indication)

    # assumes it is a WesternPitch name
    elif (
        pitch_indication[0] in music_parameters.constants.DIATONIC_PITCH_CLASS_CONTAINER
    ):
        if pitch_indication[-1].isdigit():
            pitch_name, octave = pitch_indication[:-1], int(pitch_indication[-1])
            pitch = music_parameters.WesternPitch(pitch_name, octave)
        else:
            pitch = music_parameters.WesternPitch(pitch_indication)

        return pitch

    else:
        raise NotImplementedError(
            f"Can't build pitch from pitch_indication '{pitch_indication}'."
            " Supported string formats are (1) ratios divided by a forward "
            "slash (for instance '3/2' or '4/3') and (2) names of western "
            "pitch classes with an optional number to indicate the octave "
            "(for instance 'c4', 'as' or 'fqs2')."
        )


UNKNOWN_OBJECT_TO_PITCH_LIST = _unknown_object_to_pitch_list
"""This function converts any input parameter for the `pitch_list`
property to a list of :class:`mutwo.music_parameters.abc.Pitch` objects.
It is used inside :class:`mutwo.music_events.NoteLike` in order to allow
syntactic sugar when parsing pitches to `NoteLike`. This functions
allows the following syntax:


    >>> music_events.NoteLike('c d f') # or
    >>> music_events.NoteLike('3/2')

It can be overridden by the user if desired.
"""


def _unknown_object_to_volume(volume: typing.Any) -> music_parameters.abc.Volume:
    match volume:
        case music_parameters.abc.Volume():
            volume = volume
        case numbers.Real():
            if volume >= 0:  # type: ignore
                volume = music_parameters.DirectVolume(volume)  # type: ignore
            else:
                volume = music_parameters.DecibelVolume(volume)  # type: ignore
        case str():
            volume = music_parameters.WesternVolume(volume)
        case _:
            raise TypeError(
                "Can't initialise '{}' with value '{}' of type '{}' for argument"
                " 'volume'. The type for 'volume' should be '{}'.".format(
                    type(self).__name__, volume, type(volume), Volume
                )
            )
    return volume


UNKNOWN_OBJECT_TO_VOLUME = _unknown_object_to_volume
"""This function is called when any object is assigned to
the `volume` property of :class:`mutwo.music_events.NoteLike`.
The function is called on the object which is tried to be assigned
to the volume property. The function tries to return an instance
of :class:`mutwo.music_parameters.abc.Volume` or an instance
of any child class. The aim of this function is to allow syntactic
sugar to the user. For instance consider the following:


    >>> music_events.NoteLike('3/2', 'p')

Here the volume property is 'p'. This is merely a string and
not a volume object. The function `UNKNOWN_OBJECT_TO_VOLUME`
automatically converts the string 'p' to
`music_parameters.WesternVolume('p')`. User can override the
default conversion routine.

You can compare `mutwo.core_events.UNKNOWN_OBJECT_TO_DURATION`
and `UNKNOWN_OBJECT_TO_PITCH` and
`UNKNOWN_OBJECT_TO_GRACE_NOTE_SEQUENTIAL_EVENT` for similar
functions."""


GraceNotes = core_events.SequentialEvent[core_events.SimpleEvent]


def _unknown_object_to_grace_note_sequential_event(
    unknown_object: GraceNotes | core_events.SimpleEvent,
) -> GraceNotes:
    match unknown_object:
        case core_events.SimpleEvent():
            return core_events.SequentialEvent([unknown_object])
        case core_events.SequentialEvent():
            return unknown_object
        case _:
            raise TypeError(f"Can't set grace notes to {unknown_object}")


UNKNOWN_OBJECT_TO_GRACE_NOTE_SEQUENTIAL_EVENT = (
    _unknown_object_to_grace_note_sequential_event
)
"""Convert any object to a :class:`mutwo.core_events.SequentialEvent`.
This function is used inside :class:`mutwo.music_events.NoteLike`. It
helps to allow syntactic sugar and raises errors for unsupported types.
It can be overridden by the user."""
