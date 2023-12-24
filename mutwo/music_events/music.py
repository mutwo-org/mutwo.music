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
    """:class:`NoteLike` can be a tone, chord, percussion note or rest.

    :param pitch_list: The pitch or pitches of the event. This can
        be a pitch object (any class that inherits from :class:`~mutwo.music_parameters.abc.Pitch`)
        or a list of pitch objects. Furthermore :mod:`mutwo` supports syntactic sugar
        to convert other objects on the fly to pitch objects: A string can be
        read as pitch class names to build
        :class:`mutwo.music_parameters.WesternPitch` objects or as ratios to
        build :class:`mutwo.music_parameters.JustIntonationPitch` objects.
        Fraction will also build :class:`mutwo.music_parameters.JustIntonationPitch`
        objects. Other numbers (integer and float) will be read as pitch class numbers
        to make :class:`mutwo.music_parameters.WesternPitch` objects.
    :type pitch_list: PitchOrPitchSequence
    :param duration: The duration of :class:`NoteLike`.
    :type duration: mutwo.core_constants.DurationType
    :param volume: The volume of the event. Can either be a object of
        :mod:`mutwo.music_parameters.abc.Volume`, a number or a string. If the number
        ranges from 0 to 1, :mod:`mutwo` automatically generates a
        :class:`mutwo.music_parameters.DirectVolume` object (and the number
        is interpreted as the amplitude). If the number is smaller than 0,
        :mod:`mutwo` automatically generates a
        :class:`mutwo.music_parameters.volumes.DecibelVolume` (and the number
        is interpreted as `decibel <https://en.wikipedia.org/wiki/Decibel>`_). If the argument is a string,
        `mutwo` initialises a :class:`mutwo.music_parameters.volumes.WesternVolume`.
    :type volume: Volume
    :param grace_note_sequential_event: Specify `grace notes <https://en.wikipedia.org/wiki/Grace_note>`_
        which are played before the :class:`NoteLike`. If the :class:`~mutwo.core_events.SequentialEvent`
        is empty, no grace notes are present.
    :type grace_note_sequential_event: core_events.SequentialEvent[NoteLike]
    :param after_grace_note_sequential_event: Specify `grace notes <https://en.wikipedia.org/wiki/Grace_note>`_
        which are played after the :class:`NoteLike`. If the :class:`~mutwo.core_events.SequentialEvent`
        is empty, no grace notes are present.
    :type after_grace_note_sequential_event: core_events.SequentialEvent[NoteLike]
    :param playing_indicator_collection: A :class:`~mutwo.music_parameters.playing_indicator_collection.PlayingIndicatorCollection`.
        Playing indicators alter the sound of :class:`NoteLike` (e.g.
        tremolo, fermata, pizzicato).
    :type playing_indicator_collection: music_parameters.playing_indicator_collection.PlayingIndicatorCollection
    :param notation_indicator_collection: A :class:`~mutwo.music_parameters.notation_indicator_collection.NotationIndicatorCollection`.
        Notation indicators alter the visual representation of :class:`NoteLike`
        (e.g. ottava, clefs) without affecting the resulting sound.
    :type notation_indicator_collection: music_parameters.notation_indicator_collection.NotationIndicatorCollection
    :param lyric: If with this :class:`NoteLike` a text is to be sung or spoken,
        this text can be specified here. Default to ``music_parameters.DirectLyric("")``.
    :type lyric: core_parameters.abc.Lyric
    :param instrument_list: If an event is played with one or more specifc
        :class:`mutwo.music_parameters.abc.Instrument`, these instruments can be
        assigned here. Default is an empty list.
    :type instrument_list: list[music_parameters.abc.Instrument]

    ``mutwo.music`` doesn't differentiate between tones, chords and
    rests, but rather simply implements one general class that can
    represent any of the mentioned definitions (e.g. a `NoteLike`
    with several pitches may be called a 'chord' and a `NoteLike`
    with only one pitch may be called a 'tone').

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
        self.playing_indicator_collection = playing_indicator_collection
        self.notation_indicator_collection = notation_indicator_collection
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
        """The :class:`~mutwo.music_parameters.abc.Volume` of the event."""
        return self._volume

    @volume.setter
    def volume(self, volume: typing.Any):
        self._volume = music_events.configurations.UNKNOWN_OBJECT_TO_VOLUME(volume)

    @property
    def grace_note_sequential_event(self) -> GraceNotes:
        """:class:`~mutwo.core_events.SequentialEvent` before :class:`NoteLike`"""
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
        """:class:`~mutwo.core_events.SequentialEvent` after :class:`NoteLike`"""
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

    @property
    def playing_indicator_collection(
        self,
    ) -> music_parameters.PlayingIndicatorCollection:
        return self._playing_indicator_collection

    @playing_indicator_collection.setter
    def playing_indicator_collection(
        self,
        playing_indicator_collection: typing.Optional[
            music_parameters.PlayingIndicatorCollection | str
        ],
    ):
        self._playing_indicator_collection = (
            music_events.configurations.UNKNOWN_OBJECT_TO_PLAYING_INDICATOR_COLLECTION(
                playing_indicator_collection
            )
        )

    @property
    def notation_indicator_collection(
        self,
    ) -> music_parameters.NotationIndicatorCollection:
        return self._notation_indicator_collection

    @notation_indicator_collection.setter
    def notation_indicator_collection(
        self,
        notation_indicator_collection: typing.Optional[
            music_parameters.NotationIndicatorCollection | str
        ],
    ):
        self._notation_indicator_collection = (
            music_events.configurations.UNKNOWN_OBJECT_TO_NOTATION_INDICATOR_COLLECTION(
                notation_indicator_collection
            )
        )
