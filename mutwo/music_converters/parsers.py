"""Standardization for transformations between parameters and simple events

All converters here expect by default a :class:`mutwo.music_events.NoteLike`
(and uses the attribute names defined for the
:class:`mutwo.music_events.NoteLike`). To adjust the used names you can change
the values in the :mod:`mutwo.music_converters.configurations` module.
"""

import abc
import typing

from mutwo import core_converters
from mutwo import core_events
from mutwo import music_converters
from mutwo import music_events
from mutwo import music_parameters


__all__ = (
    "SimpleEventToPitchList",
    "SimpleEventToVolume",
    "SimpleEventToLyric",
    "SimpleEventToInstrumentList",
    "SimpleEventToPlayingIndicatorCollection",
    "SimpleEventToNotationIndicatorCollection",
    "SimpleEventToGraceNoteSequentialEvent",
    "SimpleEventToAfterGraceNoteSequentialEvent",
    "MutwoParameterDictToPitchList",
    "MutwoParameterDictToVolume",
    "MutwoParameterDictToInstrumentList",
    "MutwoParameterDictToPlayingIndicatorCollection",
    "MutwoParameterDictToNotationIndicatorCollection",
    "MutwoParameterDictToGraceNoteSequentialEvent",
    "MutwoParameterDictToAfterGraceNoteSequentialEvent",
    "MutwoParameterDictToNoteLike",
)


class SimpleEventToPitchList(core_converters.SimpleEventToAttribute):
    def __init__(
        self,
        attribute_name: typing.Optional[str] = None,
        exception_value: list[music_parameters.abc.Pitch] = [],
    ):
        super().__init__(
            attribute_name
            or music_converters.configurations.DEFAULT_PITCH_LIST_TO_SEARCH_NAME,
            exception_value,
        )


class SimpleEventToVolume(core_converters.SimpleEventToAttribute):
    def __init__(
        self,
        attribute_name: typing.Optional[str] = None,
        exception_value: music_parameters.abc.Volume = music_parameters.DirectVolume(0),
    ):
        super().__init__(
            attribute_name
            or (music_converters.configurations.DEFAULT_VOLUME_TO_SEARCH_NAME),
            exception_value,
        )


class SimpleEventToLyric(core_converters.SimpleEventToAttribute):
    def __init__(
        self,
        attribute_name: typing.Optional[str] = None,
        exception_value: music_parameters.abc.Volume = music_parameters.DirectLyric(""),
    ):
        super().__init__(
            attribute_name
            or music_converters.configurations.DEFAULT_LYRIC_TO_SEARCH_NAME,
            exception_value,
        )


class SimpleEventToInstrumentList(core_converters.SimpleEventToAttribute):
    def __init__(
        self,
        attribute_name: typing.Optional[str] = None,
        exception_value: typing.Optional[music_parameters.abc.Instrument] = [],
    ):
        super().__init__(
            attribute_name
            or music_converters.configurations.DEFAULT_INSTRUMENT_LIST_TO_SEARCH_NAME,
            exception_value,
        )


class SimpleEventToAttributeWithDefaultValue(core_converters.SimpleEventToAttribute):
    @abc.abstractmethod
    def _get_default_exception_value(self) -> typing.Any:
        raise NotImplementedError

    def convert(self, *args, **kwargs) -> typing.Any:
        # If it is undefined we will use the default value.
        is_default_exception_value = self._exception_value is None

        if is_default_exception_value:
            # We use a method to get the default value (instead of e.g.
            # a class attribute), because in case the user changes the
            # value of the default value (usually defined in a constants
            # module) the change should take effect.
            self._exception_value = self._get_default_exception_value()

        attribute = super().convert(*args, **kwargs)

        if is_default_exception_value:
            self._exception_value = None

        return attribute


class SimpleEventToPlayingIndicatorCollection(SimpleEventToAttributeWithDefaultValue):
    def __init__(
        self,
        attribute_name: typing.Optional[str] = None,
        exception_value: typing.Optional[
            music_parameters.NotationIndicatorCollection
        ] = None,
    ):
        super().__init__(
            attribute_name
            or music_converters.configurations.DEFAULT_PLAYING_INDICATOR_COLLECTION_TO_SEARCH_NAME,
            exception_value,
        )

    def _get_default_exception_value(self) -> typing.Any:
        return music_events.configurations.DEFAULT_PLAYING_INDICATORS_COLLECTION_CLASS()


class SimpleEventToNotationIndicatorCollection(SimpleEventToAttributeWithDefaultValue):
    def __init__(
        self,
        attribute_name: typing.Optional[str] = None,
        exception_value: typing.Optional[
            music_parameters.NotationIndicatorCollection
        ] = None,
    ):
        super().__init__(
            attribute_name
            or music_converters.configurations.DEFAULT_NOTATION_INDICATOR_COLLECTION_TO_SEARCH_NAME,
            exception_value,
        )

    def _get_default_exception_value(self) -> typing.Any:
        return (
            music_events.configurations.DEFAULT_NOTATION_INDICATORS_COLLECTION_CLASS()
        )


class SimpleEventToGraceNoteSequentialEvent(core_converters.SimpleEventToAttribute):
    def __init__(
        self,
        attribute_name: typing.Optional[str] = None,
        exception_value: core_events.SequentialEvent = core_events.SequentialEvent([]),
    ):
        super().__init__(
            attribute_name
            or music_converters.configurations.DEFAULT_GRACE_NOTE_SEQUENTIAL_EVENT_TO_SEARCH_NAME,
            exception_value,
        )


class SimpleEventToAfterGraceNoteSequentialEvent(
    core_converters.SimpleEventToAttribute
):
    def __init__(
        self,
        attribute_name: typing.Optional[str] = None,
        exception_value: core_events.SequentialEvent = core_events.SequentialEvent([]),
    ):
        super().__init__(
            attribute_name
            or music_converters.configurations.DEFAULT_AFTER_GRACE_NOTE_SEQUENTIAL_EVENT_TO_SEARCH_NAME,
            exception_value,
        )


class MutwoParameterDictToPitchList(
    core_converters.MutwoParameterDictToKeywordArgument
):
    def __init__(
        self,
        pitch_list_to_search_name: typing.Optional[str] = None,
        pitch_list_keyword_name: typing.Optional[str] = None,
    ):
        super().__init__(
            pitch_list_to_search_name
            or music_converters.configurations.DEFAULT_PITCH_LIST_TO_SEARCH_NAME,
            pitch_list_keyword_name
            or music_converters.configurations.DEFAULT_PITCH_LIST_KEYWORD_NAME,
        )


class MutwoParameterDictToVolume(core_converters.MutwoParameterDictToKeywordArgument):
    def __init__(
        self,
        volume_to_search_name: typing.Optional[str] = None,
        volume_keyword_name: typing.Optional[str] = None,
    ):
        super().__init__(
            volume_to_search_name
            or music_converters.configurations.DEFAULT_VOLUME_TO_SEARCH_NAME,
            volume_keyword_name
            or music_converters.configurations.DEFAULT_VOLUME_KEYWORD_NAME,
        )


class MutwoParameterDictToInstrumentList(
    core_converters.MutwoParameterDictToKeywordArgument
):
    def __init__(
        self,
        instrument_list_to_search_name: typing.Optional[str] = None,
        instrument_list_keyword_name: typing.Optional[str] = None,
    ):
        super().__init__(
            instrument_list_to_search_name
            or music_converters.configurations.DEFAULT_INSTRUMENT_LIST_TO_SEARCH_NAME,
            instrument_list_keyword_name
            or music_converters.configurations.DEFAULT_INSTRUMENT_LIST_KEYWORD_NAME,
        )


class MutwoParameterDictToPlayingIndicatorCollection(
    core_converters.MutwoParameterDictToKeywordArgument
):
    def __init__(
        self,
        playing_indicator_collection_to_search_name: typing.Optional[str] = None,
        playing_indicator_collection_keyword_name: typing.Optional[str] = None,
    ):
        super().__init__(
            playing_indicator_collection_to_search_name
            or music_converters.configurations.DEFAULT_PLAYING_INDICATOR_COLLECTION_TO_SEARCH_NAME,
            playing_indicator_collection_keyword_name
            or music_converters.configurations.DEFAULT_PLAYING_INDICATOR_COLLECTION_KEYWORD_NAME,
        )


class MutwoParameterDictToNotationIndicatorCollection(
    core_converters.MutwoParameterDictToKeywordArgument
):
    def __init__(
        self,
        notation_indicator_collection_to_search_name: typing.Optional[str] = None,
        notation_indicator_collection_keyword_name: typing.Optional[str] = None,
    ):
        super().__init__(
            notation_indicator_collection_to_search_name
            or music_converters.configurations.DEFAULT_NOTATION_INDICATOR_COLLECTION_TO_SEARCH_NAME,
            notation_indicator_collection_keyword_name
            or music_converters.configurations.DEFAULT_NOTATION_INDICATOR_COLLECTION_KEYWORD_NAME,
        )


class MutwoParameterDictToGraceNoteSequentialEvent(
    core_converters.MutwoParameterDictToKeywordArgument
):
    def __init__(
        self,
        grace_note_sequential_event_to_search_name: typing.Optional[str] = None,
        grace_note_sequential_event_keyword_name: typing.Optional[str] = None,
    ):
        super().__init__(
            grace_note_sequential_event_to_search_name
            or music_converters.configurations.DEFAULT_GRACE_NOTE_SEQUENTIAL_EVENT_TO_SEARCH_NAME,
            grace_note_sequential_event_keyword_name
            or music_converters.configurations.DEFAULT_GRACE_NOTE_SEQUENTIAL_EVENT_KEYWORD_NAME,
        )


class MutwoParameterDictToAfterGraceNoteSequentialEvent(
    core_converters.MutwoParameterDictToKeywordArgument
):
    def __init__(
        self,
        after_grace_note_sequential_event_to_search_name: typing.Optional[str] = None,
        after_grace_note_sequential_event_keyword_name: typing.Optional[str] = None,
    ):
        super().__init__(
            after_grace_note_sequential_event_to_search_name
            or music_converters.configurations.DEFAULT_AFTER_GRACE_NOTE_SEQUENTIAL_EVENT_TO_SEARCH_NAME,
            after_grace_note_sequential_event_keyword_name
            or music_converters.configurations.DEFAULT_AFTER_GRACE_NOTE_SEQUENTIAL_EVENT_KEYWORD_NAME,
        )


class MutwoParameterDictToNoteLike(core_converters.MutwoParameterDictToSimpleEvent):
    """Convert a dict of mutwo parameters to a :class:`mutwo.music_events.NoteLike`

    :param mutwo_parameter_dict_to_keyword_argument_sequence: A sequence of
        :class:`MutwoParameterDictToKeywordArgument`.
        Default to `None`.
    :type mutwo_parameter_dict_to_keyword_argument_sequence: typing.Optional[typing.Sequence[MutwoParameterDictToKeywordArgument]]
    :param simple_event_class: Default to :class:`mutwo.music_events.NoteLike`.
    :type simple_event_class: typing.Type[core_events.SimpleEvent]
    """

    def __init__(
        self,
        mutwo_parameter_dict_to_keyword_argument_sequence: typing.Optional[
            typing.Sequence[core_converters.MutwoParameterDictToKeywordArgument]
        ] = None,
        simple_event_class: typing.Type[
            core_events.SimpleEvent
        ] = music_events.NoteLike,
    ):
        if mutwo_parameter_dict_to_keyword_argument_sequence is None:
            mutwo_parameter_dict_to_keyword_argument_sequence = (
                core_converters.MutwoParameterDictToDuration(),
                MutwoParameterDictToPitchList(),
                MutwoParameterDictToVolume(),
                MutwoParameterDictToPlayingIndicatorCollection(),
                MutwoParameterDictToNotationIndicatorCollection(),
                MutwoParameterDictToGraceNoteSequentialEvent(),
                MutwoParameterDictToAfterGraceNoteSequentialEvent(),
                MutwoParameterDictToInstrumentList(),
            )
        super().__init__(
            mutwo_parameter_dict_to_keyword_argument_sequence, simple_event_class
        )
