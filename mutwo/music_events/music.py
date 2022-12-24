"""Event classes which are designated for musical usage."""

import typing

from mutwo import core_events
from mutwo import core_constants
from mutwo import music_events
from mutwo import music_parameters

__all__ = ("NoteLike",)

PitchOrPitchSequence = (
    music_parameters.abc.Pitch | typing.Sequence | core_constants.Real | None
)

Volume = music_parameters.abc.Volume | core_constants.Real | str
GraceNotes = core_events.SequentialEvent[core_events.SimpleEvent]


class NoteLike(core_events.SimpleEvent):
    """:class:`NoteLike` represents traditional discreet musical objects.

    :param pitch_list: The pitch or pitches of the event. This can
        be a pitch object (any class that inherits from ``mutwo.music_parameters.abc.Pitch``)
        or a list of pitch objects. Furthermore mutwo supports syntactic sugar
        to convert other objects on the fly to pitch objects: Atring can be
        read as pitch class names to build
        :class:`mutwo.music_parameters.WesternPitch` objects or as ratios to
        build :class:`mutwo.music_parameters.JustIntonationPitch` objects.
        Fraction will also build :class:`mutwo.music_parameters.JustIntonationPitch`
        objects. Other numbers (integer and float) will be read as pitch class numbers
        to make :class:`mutwo.music_parameters.WesternPitch` objects.
    :param duration: The duration of ``NoteLike``. This can be any number.
        The unit of the duration is up to the interpretation of the user and the
        respective converter routine that will be used.
    :param volume: The volume of the event. Can either be a object of
        :mod:`mutwo.music_parameters.abc.Volume`, a number or a string. If the number
        ranges from 0 to 1, mutwo automatically generates a
        :class:`mutwo.music_parameters.DirectVolume` object (and the number
        will be interpreted as the amplitude). If the
        number is smaller than 0, automatically generates a
        :class:`mutwo.music_parameters.volumes.DecibelVolume` object (and the number
        will be interpreted as decibel). If the argument is a string,
        `mutwo` will try to initialise a :class:`mutwo.music_parameters.volumes.WesternVolume`
        object.
    :param grace_note_sequential_event:
    :type grace_note_sequential_event: core_events.SequentialEvent[NoteLike]
    :param after_grace_note_sequential_event:
    :type after_grace_note_sequential_event: core_events.SequentialEvent[NoteLike]
    :param playing_indicator_collection: A :class:`~mutwo.music_parameters.playing_indicator_collection.PlayingIndicatorCollection`.
        Playing indicators alter the sound of :class:`NoteLike` (e.g.
        tremolo, fermata, pizzicato).
    :type playing_indicator_collection: music_parameters.playing_indicator_collection.PlayingIndicatorCollection
    :param notation_indicator_collection: A :class:`~mutwo.music_parameters.notation_indicator_collection.NotationIndicatorCollection`.
        Notation indicators alter the visual representation of :class:`NoteLike`
        (e.g. ottava, clefs) without affecting the resulting sound.
    :type notation_indicator_collection: music_parameters.notation_indicator_collection.NotationIndicatorCollection
    :param lyric:
    :type lyric: core_parameters.abc.Lyric
    :param instrument_list: If an event is played with one or more specifc
        :class:`mutwo.music_parameters.abc.Instrument`, these instruments can be
        assigned here. Default is an empty list.
    :type instrument_list: list[music_parameters.abc.Instrument]

    ``mutwo.music`` doesn't differentiate between Tones, Chords and
    Rests, but rather simply implements one general class which can
    represent any of the mentioned definitions (e.g. a `NoteLike` object
    with several pitches may be called a 'Chord' and a `NoteLike` object
    with only one pitch may be called a 'Tone').

    **Example:**

    >>> from mutwo import music_parameters
    >>> from mutwo import music_events
    >>> tone = music_events.NoteLike(music_parameters.WesternPitch('a'), 1, 1)
    >>> other_tone = music_events.NoteLike('3/2', 1, 0.5)
    >>> chord = music_events.NoteLike(
    ...     [music_parameters.WesternPitch('a'), music_parameters.JustIntonationPitch('3/2')], 1, 1
    ... )
    >>> other_chord = music_events.NoteLike('c4 dqs3 10/7', 1, 3)
    """

    def __init__(
        self,
        pitch_list: PitchOrPitchSequence = [],
        duration: core_constants.DurationType = 1,
        volume: Volume = "mf",
        grace_note_sequential_event: typing.Optional[GraceNotes] = None,
        after_grace_note_sequential_event: typing.Optional[GraceNotes] = None,
        playing_indicator_collection: typing.Optional[
            music_parameters.PlayingIndicatorCollection
        ] = None,
        notation_indicator_collection: typing.Optional[
            music_parameters.NotationIndicatorCollection
        ] = None,
        lyric: music_parameters.abc.Lyric = music_parameters.DirectLyric(""),
        instrument_list: list[music_parameters.abc.Instrument] = [],
    ):
        self.pitch_list = pitch_list
        self.volume = volume
        super().__init__(duration)
        self.grace_note_sequential_event = (
            grace_note_sequential_event or core_events.SequentialEvent([])
        )
        self.after_grace_note_sequential_event = (
            after_grace_note_sequential_event or core_events.SequentialEvent([])
        )
        self.playing_indicator_collection = (
            playing_indicator_collection
            or music_events.configurations.DEFAULT_PLAYING_INDICATORS_COLLECTION_CLASS()
        )
        self.notation_indicator_collection = (
            notation_indicator_collection
            or music_events.configurations.DEFAULT_NOTATION_INDICATORS_COLLECTION_CLASS()
        )
        self.lyric = lyric
        self.instrument_list = instrument_list

    # ###################################################################### #
    #                            properties                                  #
    # ###################################################################### #

    @property
    def _parameter_to_print_tuple(self) -> tuple[str, ...]:
        """Return tuple of attribute names which shall be printed for repr."""
        return tuple(
            attribute
            for attribute in self._parameter_to_compare_tuple
            if attribute
            # Avoid too verbose and long attributes
            not in (
                "playing_indicator_collection",
                "notation_indicator_collection",
                "grace_note_sequential_event",
                "after_grace_note_sequential_event",
            )
        )

    @property
    def pitch_list(self) -> typing.Any:
        """The pitch or pitches of the event."""

        return self._pitch_list

    @pitch_list.setter
    def pitch_list(self, pitch_list: typing.Any):
        # make sure pitch_list always become assigned to a list of pitches,
        # to be certain of the returned type
        if not isinstance(pitch_list, str) and isinstance(pitch_list, typing.Iterable):
            parsed_pitch_list = []
            for pitch in pitch_list:
                parsed_pitch_list.extend(
                    music_events.configurations.UNKNOWN_OBJECT_TO_PITCH_LIST(pitch)
                )
            pitch_list = parsed_pitch_list
        else:
            pitch_list = music_events.configurations.UNKNOWN_OBJECT_TO_PITCH_LIST(
                pitch_list
            )

        self._pitch_list = pitch_list

    @property
    def volume(self) -> typing.Any:
        """The volume of the event."""
        return self._volume

    @volume.setter
    def volume(self, volume: typing.Any):
        self._volume = music_events.configurations.UNKNOWN_OBJECT_TO_VOLUME(volume)

    @property
    def grace_note_sequential_event(self) -> GraceNotes:
        """:class:`core_events.SequentialEvent` before :class:`NoteLike`"""
        return self._grace_note_sequential_event

    @grace_note_sequential_event.setter
    def grace_note_sequential_event(
        self,
        grace_note_sequential_event: GraceNotes | core_events.SimpleEvent,
    ):
        self._grace_note_sequential_event = (
            music_events.configurations.UNKNOWN_OBJECT_TO_GRACE_NOTE_SEQUENTIAL_EVENT(
                grace_note_sequential_event
            )
        )

    @property
    def after_grace_note_sequential_event(self) -> GraceNotes:
        """:class:`core_events.SequentialEvent` after :class:`NoteLike`"""
        return self._after_grace_note_sequential_event

    @after_grace_note_sequential_event.setter
    def after_grace_note_sequential_event(
        self, after_grace_note_sequential_event: GraceNotes | core_events.SimpleEvent
    ):
        self._after_grace_note_sequential_event = (
            music_events.configurations.UNKNOWN_OBJECT_TO_GRACE_NOTE_SEQUENTIAL_EVENT(
                after_grace_note_sequential_event
            )
        )
