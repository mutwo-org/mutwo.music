"""Standardised way to extract data from simple events.

All converters here expect by default a:class:`mutwo.music_events.NoteLike`
(and uses the attribute names defined for the
:class:`mutwo.music_events.NoteLike`).
"""

import abc
import typing

from mutwo import core_converters
from mutwo import core_events
from mutwo import music_events
from mutwo import music_parameters


__all__ = (
    "SimpleEventToPitchList",
    "SimpleEventToVolume",
    "SimpleEventToPlayingIndicatorCollection",
    "SimpleEventToNotationIndicatorCollection",
    "SimpleEventToGraceNoteSequentialEvent",
    "SimpleEventToAfterGraceNoteSequentialEvent",
)


class SimpleEventToPitchList(core_converters.SimpleEventToAttribute):
    def __init__(
        self,
        attribute_name: str = "pitch_list",
        exception_value: list[music_parameters.abc.Pitch] = [],
    ):
        super().__init__(attribute_name, exception_value)


class SimpleEventToVolume(core_converters.SimpleEventToAttribute):
    def __init__(
        self,
        attribute_name: str = "volume",
        exception_value: music_parameters.abc.Volume = music_parameters.DirectVolume(0),
    ):
        super().__init__(attribute_name, exception_value)


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
        attribute_name: str = "playing_indicator_collection",
        exception_value: typing.Optional[
            music_parameters.NotationIndicatorCollection
        ] = None,
    ):
        super().__init__(attribute_name, exception_value)

    def _get_default_exception_value(self) -> typing.Any:
        return music_events.constants.DEFAULT_PLAYING_INDICATORS_COLLECTION_CLASS()


class SimpleEventToNotationIndicatorCollection(SimpleEventToAttributeWithDefaultValue):
    def __init__(
        self,
        attribute_name: str = "notation_indicator_collection",
        exception_value: typing.Optional[
            music_parameters.NotationIndicatorCollection
        ] = None,
    ):
        super().__init__(attribute_name, exception_value)

    def _get_default_exception_value(self) -> typing.Any:
        return music_events.constants.DEFAULT_NOTATION_INDICATORS_COLLECTION_CLASS()


class SimpleEventToGraceNoteSequentialEvent(core_converters.SimpleEventToAttribute):
    def __init__(
        self,
        attribute_name: str = "grace_note_sequential_event",
        exception_value: core_events.SequentialEvent = core_events.SequentialEvent([]),
    ):
        super().__init__(attribute_name, exception_value)


class SimpleEventToAfterGraceNoteSequentialEvent(
    core_converters.SimpleEventToAttribute
):
    def __init__(
        self,
        attribute_name: str = "after_grace_note_sequential_event",
        exception_value: core_events.SequentialEvent = core_events.SequentialEvent([]),
    ):
        super().__init__(attribute_name, exception_value)
