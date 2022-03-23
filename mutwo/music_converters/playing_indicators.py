"""Apply :class:`~mutwo.music_parameters.abc.PlayingIndicator` on :class:`~mutwo.core_events.abc.Event`.

"""

import abc
import copy
import itertools
import typing
import warnings

try:
    import quicktions as fractions  # type: ignore
except ImportError:
    import fractions  # type: ignore

from mutwo import core_constants
from mutwo import core_converters
from mutwo import core_events
from mutwo import core_utilities
from mutwo import music_events
from mutwo import music_parameters


__all__ = (
    "PlayingIndicatorConverter",
    "ArpeggioConverter",
    "StacattoConverter",
    "ArticulationConverter",
    "TrillConverter",
    "PlayingIndicatorsConverter",
)


class PlayingIndicatorConverter(core_converters.abc.Converter):
    """Abstract base class to apply :class:`~mutwo.music_parameters.abc.PlayingIndicator` on a :class:`~mutwo.core_events.SimpleEvent`.

    :param simple_event_to_playing_indicator_collection: Function to extract from a
        :class:`mutwo.core_events.SimpleEvent` a
        :class:`mutwo.music_parameters.PlayingIndicatorCollection`
        object. By default it asks the Event for its
        :attr:`~mutwo.ext.events.music.NoteLike.playing_indicator_collection`
        attribute (because by default :class:`mutwo.ext.events.music.NoteLike`
        objects are expected).
        When using different Event classes than :class:`~mutwo.ext.events.music.NoteLike`
        with a different name for their playing_indicator_collection property, this argument
        should be overridden. If the
        function call raises an :obj:`AttributeError` (e.g. if no playing indicator
        collection can be extracted), mutwo will build a playing indicator collection
        from :const:`~mutwo.music_events.configurations.DEFAULT_PLAYING_INDICATORS_COLLECTION_CLASS`.
    :type simple_event_to_playing_indicator_collection: typing.Callable[[core_events.SimpleEvent], music_parameters.PlayingIndicatorCollection], optional

    To write a new PlayingIndicatorConverter the abstract method
    :func:`_apply_playing_indicator` and the abstract properties
    `playing_indicator_name` and `default_playing_indicator` have
    to be overridden.
    """

    def __init__(
        self,
        simple_event_to_playing_indicator_collection: typing.Callable[
            [core_events.SimpleEvent],
            music_parameters.PlayingIndicatorCollection,
        ] = lambda simple_event: simple_event.playing_indicator_collection,  # type: ignore
    ):
        self._simple_event_to_playing_indicator_collection = (
            simple_event_to_playing_indicator_collection
        )

    @abc.abstractmethod
    def _apply_playing_indicator(
        self,
        simple_event_to_convert: core_events.SimpleEvent,
        playing_indicator: music_parameters.abc.PlayingIndicator,
    ) -> core_events.SequentialEvent[core_events.SimpleEvent]:
        raise NotImplementedError()

    @property
    @abc.abstractmethod
    def playing_indicator_name(self) -> str:
        raise NotImplementedError()

    @property
    @abc.abstractmethod
    def default_playing_indicator(self) -> music_parameters.abc.PlayingIndicator:
        raise NotImplementedError

    def convert(
        self, simple_event_to_convert: core_events.SimpleEvent
    ) -> core_events.SequentialEvent[core_events.SimpleEvent]:
        """Apply PlayingIndicator on simple_event.

        :param simple_event_to_convert: The event which shall be converted.
        :type simple_event_to_convert: core_events.SimpleEvent
        """

        playing_indicator_collection = core_utilities.call_function_except_attribute_error(
            self._simple_event_to_playing_indicator_collection,
            simple_event_to_convert,
            music_events.configurations.DEFAULT_PLAYING_INDICATORS_COLLECTION_CLASS(),
        )
        playing_indicator = core_utilities.call_function_except_attribute_error(
            lambda playing_indicator_collection: getattr(
                playing_indicator_collection, self.playing_indicator_name
            ),
            playing_indicator_collection,
            self.default_playing_indicator,
        )

        if playing_indicator.is_active:
            return self._apply_playing_indicator(
                simple_event_to_convert, playing_indicator
            )
        else:
            return core_events.SequentialEvent([copy.deepcopy(simple_event_to_convert)])


class ArpeggioConverter(PlayingIndicatorConverter):
    """Apply arpeggio on :class:`~mutwo.core_events.SimpleEvent`.

    :param duration_for_each_attack: Set how long each attack of the
        Arpeggio lasts. Default to 0.1.
    :type duration_for_each_attack: constants.DurationType
    :param simple_event_to_pitch_list: Function to extract from a
        :class:`mutwo.core_events.SimpleEvent` a tuple that contains pitch objects
        (objects that inherit from :class:`mutwo.music_parameters.abc.Pitch`).
        By default it asks the Event for its
        :attr:`~mutwo.ext.events.music.NoteLike.pitch_list` attribute
        (because by default :class:`mutwo.ext.events.music.NoteLike` objects are expected).
        When using different Event classes than :class:`~mutwo.ext.events.music.NoteLike`
        with a different name for their pitch property, this argument
        should be overridden.
        If the function call raises an :obj:`AttributeError` (e.g. if no pitch can be
        extracted), mutwo will assume an event without any pitches.
    :type simple_event_to_pitch_list: typing.Callable[[core_events.SimpleEvent], music_parameters.abc.Pitch], optional
    :param simple_event_to_playing_indicator_collection: Function to extract from a
        :class:`mutwo.core_events.SimpleEvent` a
        :class:`mutwo.music_parameters.PlayingIndicatorCollection`
        object. By default it asks the Event for its
        :attr:`~mutwo.ext.events.music.NoteLike.playing_indicator_collection`
        attribute (because by default :class:`mutwo.ext.events.music.NoteLike`
        objects are expected).
        When using different Event classes than :class:`~mutwo.ext.events.music.NoteLike`
        with a different name for their playing_indicator_collection property, this argument
        should be overridden. If the
        function call raises an :obj:`AttributeError` (e.g. if no playing indicator
        collection can be extracted), mutwo will build a playing indicator collection
        from :const:`~mutwo.music_events.configurations.DEFAULT_PLAYING_INDICATORS_COLLECTION_CLASS`.
    :type simple_event_to_playing_indicator_collection: typing.Callable[[core_events.SimpleEvent], music_parameters.PlayingIndicatorCollection,], optional
    :param set_pitch_list_for_simple_event: Function which assigns
        a list of :class:`~mutwo.music_parameters.abc.Pitch` objects to a
        :class:`~mutwo.core_events.SimpleEvent`. By default the
        function assigns the passed pitches to the
        :attr:`~mutwo.ext.events.music.NoteLike.pitch_list` attribute
        (because by default :class:`mutwo.ext.events.music.NoteLike` objects
        are expected).
    :type set_pitch_list_for_simple_event: typing.Callable[[core_events.SimpleEvent, list[music_parameters.abc.Pitch]], None]
    """

    def __init__(
        self,
        duration_for_each_attack: core_constants.DurationType = 0.1,
        simple_event_to_pitch_list: typing.Callable[
            [core_events.SimpleEvent], list[music_parameters.abc.Pitch]
        ] = lambda simple_event: simple_event.pitch_list,  # type: ignore
        simple_event_to_playing_indicator_collection: typing.Callable[
            [core_events.SimpleEvent],
            music_parameters.PlayingIndicatorCollection,
        ] = lambda simple_event: simple_event.playing_indicator_collection,  # type: ignore
        set_pitch_list_for_simple_event: typing.Callable[
            [core_events.SimpleEvent, list[music_parameters.abc.Pitch]], None
        ] = lambda simple_event, pitch_list: simple_event.set_parameter(  # type: ignore
            "pitch_list", pitch_list, set_unassigned_parameter=True
        ),
    ):
        super().__init__(
            simple_event_to_playing_indicator_collection=simple_event_to_playing_indicator_collection
        )
        self._duration_for_each_attack = duration_for_each_attack
        self._simple_event_to_pitch_list = simple_event_to_pitch_list
        self._set_pitch_list_for_simple_event = set_pitch_list_for_simple_event

    @property
    def playing_indicator_name(self) -> str:
        return "arpeggio"

    @property
    def default_playing_indicator(self) -> music_parameters.abc.PlayingIndicator:
        return music_parameters.Arpeggio()

    def _apply_playing_indicator(
        self,
        simple_event_to_convert: core_events.SimpleEvent,
        playing_indicator: music_parameters.Arpeggio,
    ) -> core_events.SequentialEvent[core_events.SimpleEvent]:
        try:
            pitch_list = list(self._simple_event_to_pitch_list(simple_event_to_convert))
        except AttributeError:
            pitch_list = []

        # sort pitches according to Arpeggio direction
        pitch_list.sort(reverse=playing_indicator.direction != "up")

        converted_event: core_events.SequentialEvent[
            core_events.SimpleEvent
        ] = core_events.SequentialEvent(
            [copy.copy(simple_event_to_convert) for _ in pitch_list]
        )

        # apply pitches on events
        for nth_event, pitch in enumerate(pitch_list):
            self._set_pitch_list_for_simple_event(converted_event[nth_event], [pitch])

        # set correct duration for each event
        n_events = len(converted_event)
        duration_of_each_attack = self._duration_for_each_attack
        if n_events * duration_of_each_attack > simple_event_to_convert.duration:
            duration_of_each_attack = simple_event_to_convert.duration / n_events

        for nth_event in range(n_events - 1):
            converted_event[nth_event].duration = duration_of_each_attack

        converted_event[-1].duration -= (
            converted_event.duration - simple_event_to_convert.duration
        )

        return converted_event


class StacattoConverter(PlayingIndicatorConverter):
    """Apply staccato on :class:`~mutwo.core_events.SimpleEvent`.

    :param factor:
    :param allowed_articulation_name_sequence:
    :param simple_event_to_playing_indicator_collection: Function to extract from a
        :class:`mutwo.core_events.SimpleEvent` a
        :class:`mutwo.music_parameters.PlayingIndicatorCollection`
        object. By default it asks the Event for its
        :attr:`~mutwo.ext.events.music.NoteLike.playing_indicator_collection`
        attribute (because by default :class:`mutwo.ext.events.music.NoteLike`
        objects are expected).
        When using different Event classes than :class:`~mutwo.ext.events.music.NoteLike`
        with a different name for their playing_indicator_collection property, this argument
        should be overridden. If the
        function call raises an :obj:`AttributeError` (e.g. if no playing indicator
        collection can be extracted), mutwo will build a playing indicator collection
        from :const:`~mutwo.music_events.configurations.DEFAULT_PLAYING_INDICATORS_COLLECTION_CLASS`.
    :type simple_event_to_playing_indicator_collection: typing.Callable[[core_events.SimpleEvent], music_parameters.PlayingIndicatorCollection,], optional
    """

    def __init__(
        self,
        factor: float = 0.5,
        allowed_articulation_name_sequence: typing.Sequence[str] = ("staccato", "."),
        simple_event_to_playing_indicator_collection: typing.Callable[
            [core_events.SimpleEvent],
            music_parameters.PlayingIndicatorCollection,
        ] = lambda simple_event: simple_event.playing_indicator_collection,  # type: ignore
    ):
        self._allowed_articulation_name_sequence = allowed_articulation_name_sequence
        self._factor = factor
        super().__init__(simple_event_to_playing_indicator_collection)

    def _apply_playing_indicator(
        self,
        simple_event_to_convert: core_events.SimpleEvent,
        _: music_parameters.abc.PlayingIndicator,
    ) -> core_events.SequentialEvent[core_events.SimpleEvent]:
        duration = simple_event_to_convert.duration * self._factor
        sequential_event = core_events.SequentialEvent(
            [
                simple_event_to_convert.set_parameter(
                    "duration", duration, mutate=False
                ),
                core_events.SimpleEvent(duration),
            ]
        )
        return sequential_event

    @property
    def playing_indicator_name(self) -> str:
        return "articulation"

    @property
    def default_playing_indicator(self) -> music_parameters.abc.PlayingIndicator:
        return music_parameters.Articulation()


class ArticulationConverter(PlayingIndicatorConverter):
    """Apply articulation on :class:`~mutwo.core_events.SimpleEvent`.

    :param articulation_name_tuple_to_playing_indicator_converter:
    :type articulation_name_tuple_to_playing_indicator_converter: dict[tuple[str, ...], PlayingIndicatorConverter]
    :param simple_event_to_playing_indicator_collection: Function to extract from a
        :class:`mutwo.core_events.SimpleEvent` a
        :class:`mutwo.music_parameters.PlayingIndicatorCollection`
        object. By default it asks the Event for its
        :attr:`~mutwo.ext.events.music.NoteLike.playing_indicator_collection`
        attribute (because by default :class:`mutwo.ext.events.music.NoteLike`
        objects are expected).
        When using different Event classes than :class:`~mutwo.ext.events.music.NoteLike`
        with a different name for their playing_indicator_collection property, this argument
        should be overridden. If the
        function call raises an :obj:`AttributeError` (e.g. if no playing indicator
        collection can be extracted), mutwo will build a playing indicator collection
        from :const:`~mutwo.music_events.configurations.DEFAULT_PLAYING_INDICATORS_COLLECTION_CLASS`.
    :type simple_event_to_playing_indicator_collection: typing.Callable[[core_events.SimpleEvent], music_parameters.PlayingIndicatorCollection,], optional
    """

    def __init__(
        self,
        articulation_name_tuple_to_playing_indicator_converter: dict[
            tuple[str, ...], PlayingIndicatorConverter
        ] = {("staccato", "."): StacattoConverter()},
        simple_event_to_playing_indicator_collection: typing.Callable[
            [core_events.SimpleEvent],
            music_parameters.PlayingIndicatorCollection,
        ] = lambda simple_event: simple_event.playing_indicator_collection,  # type: ignore
    ):
        articulation_name_to_playing_indicator_converter = {}
        for (
            articulation_name_tuple,
            playing_indicator_converter,
        ) in articulation_name_tuple_to_playing_indicator_converter.items():
            for articulation_name in articulation_name_tuple:
                try:
                    assert (
                        articulation_name
                        not in articulation_name_to_playing_indicator_converter
                    )
                except AssertionError:
                    warnings.warn(
                        "Found two playing indicator converter mappings for "
                        f"articulation name '{articulation_name}'! "
                        "Mutwo will use the playing indicator converter "
                        f"'{playing_indicator_converter}'."
                    )
                articulation_name_to_playing_indicator_converter.update(
                    {articulation_name: playing_indicator_converter}
                )

        self._articulation_name_to_playing_indicator_converter = (
            articulation_name_to_playing_indicator_converter
        )
        super().__init__(simple_event_to_playing_indicator_collection)

    def _apply_playing_indicator(
        self,
        simple_event_to_convert: core_events.SimpleEvent,
        playing_indicator: music_parameters.Articulation,
    ) -> core_events.SequentialEvent[core_events.SimpleEvent]:
        if (
            playing_indicator.name
            in self._articulation_name_to_playing_indicator_converter
        ):
            return self._articulation_name_to_playing_indicator_converter[
                playing_indicator.name
            ].convert(simple_event_to_convert)
        else:
            return core_events.SequentialEvent([copy.deepcopy(simple_event_to_convert)])

    @property
    def playing_indicator_name(self) -> str:
        return "articulation"

    @property
    def default_playing_indicator(self) -> music_parameters.abc.PlayingIndicator:
        return music_parameters.Articulation()


class TrillConverter(PlayingIndicatorConverter):
    """Apply trill on :class:`~mutwo.core_events.SimpleEvent`.

    :param trill_size:
    :type trill_size: constants.DurationType
    :param simple_event_to_pitch_list: Function to extract from a
        :class:`mutwo.core_events.SimpleEvent` a tuple that contains pitch objects
        (objects that inherit from :class:`mutwo.music_parameters.abc.Pitch`).
        By default it asks the Event for its
        :attr:`~mutwo.ext.events.music.NoteLike.pitch_list` attribute
        (because by default :class:`mutwo.ext.events.music.NoteLike` objects are expected).
        When using different Event classes than :class:`~mutwo.ext.events.music.NoteLike`
        with a different name for their pitch property, this argument
        should be overridden.
        If the function call raises an :obj:`AttributeError` (e.g. if no pitch can be
        extracted), mutwo will assume an event without any pitches.
    :type simple_event_to_pitch_list: typing.Callable[[core_events.SimpleEvent], music_parameters.abc.Pitch], optional
    :param simple_event_to_playing_indicator_collection: Function to extract from a
        :class:`mutwo.core_events.SimpleEvent` a
        :class:`mutwo.ext.parameters.playing_indicators.PlayingIndicatorCollection`
        object. By default it asks the Event for its
        :attr:`~mutwo.ext.events.music.NoteLike.playing_indicator_collection`
        attribute (because by default :class:`mutwo.ext.events.music.NoteLike`
        objects are expected).
        When using different Event classes than :class:`~mutwo.ext.events.music.NoteLike`
        with a different name for their playing_indicator_collection property, this argument
        should be overridden. If the
        function call raises an :obj:`AttributeError` (e.g. if no playing indicator
        collection can be extracted), mutwo will build a playing indicator collection
        from :const:`~mutwo.music_events.configurations.DEFAULT_PLAYING_INDICATORS_COLLECTION_CLASS`.
    :type simple_event_to_playing_indicator_collection: typing.Callable[[core_events.SimpleEvent], music_parameters.PlayingIndicatorCollection,], optional
    """

    def __init__(
        self,
        trill_size: core_constants.DurationType = fractions.Fraction(1, 16),
        simple_event_to_pitch_list: typing.Callable[
            [core_events.SimpleEvent], list[music_parameters.abc.Pitch]
        ] = lambda simple_event: simple_event.pitch_list,  # type: ignore
        simple_event_to_playing_indicator_collection: typing.Callable[
            [core_events.SimpleEvent],
            music_parameters.PlayingIndicatorCollection,
        ] = lambda simple_event: simple_event.playing_indicator_collection,  # type: ignore
    ):
        self._trill_size = trill_size
        self._simple_event_to_pitch_list = simple_event_to_pitch_list
        super().__init__(simple_event_to_playing_indicator_collection)

    def _apply_trill(
        self,
        simple_event_to_convert: core_events.SimpleEvent,
        trill: music_parameters.Trill,
        pitch_list: list[music_parameters.abc.Pitch],
    ) -> core_events.SequentialEvent[core_events.SimpleEvent]:
        n_trill_items = simple_event_to_convert.duration // self._trill_size
        remaining = simple_event_to_convert.duration - (
            n_trill_items * self._trill_size
        )
        sequential_event = core_events.SequentialEvent([])
        pitch_cycle = itertools.cycle((pitch_list, trill.pitch))
        for _ in range(int(n_trill_items)):
            simple_event = simple_event_to_convert.set_parameter(
                "duration", self._trill_size, mutate=False
            ).set_parameter("pitch_list", next(pitch_cycle))
            sequential_event.append(simple_event)
        sequential_event[-1].duration += remaining
        return sequential_event

    def _apply_playing_indicator(
        self,
        simple_event_to_convert: core_events.SimpleEvent,
        playing_indicator: music_parameters.Trill,
    ) -> core_events.SequentialEvent[core_events.SimpleEvent]:
        pitch_list = core_utilities.call_function_except_attribute_error(
            self._simple_event_to_pitch_list, simple_event_to_convert, []
        )
        if pitch_list:
            return self._apply_trill(
                simple_event_to_convert, playing_indicator, pitch_list
            )
        else:
            return core_events.SequentialEvent([copy.copy(simple_event_to_convert)])

    @property
    def playing_indicator_name(self) -> str:
        return "trill"

    @property
    def default_playing_indicator(self) -> music_parameters.abc.PlayingIndicator:
        return music_parameters.Trill()


class PlayingIndicatorsConverter(core_converters.abc.SymmetricalEventConverter):
    """Apply :class:`~mutwo.ext.parameters.abc.PlayingIndicator` on any :class:`~mutwo.core_events.abc.Event`.

    :param playing_indicator_converter_sequence: A sequence of :class:`PlayingIndicatorConverter` which shall
        be applied on each :class:`~mutwo.core_events.SimpleEvent`.
    :type playing_indicator_converter_sequence: typing.Sequence[PlayingIndicatorConverter]
    """

    def __init__(
        self,
        playing_indicator_converter_sequence: typing.Sequence[
            PlayingIndicatorConverter
        ],
    ):
        self._playing_indicator_converter_tuple = tuple(
            playing_indicator_converter_sequence
        )

    def _convert_simple_event(
        self,
        event_to_convert: core_events.SimpleEvent,
        _: core_constants.DurationType,
    ) -> core_events.SequentialEvent:
        """Convert instance of :class:`mutwo.core_events.SimpleEvent`."""

        converted_event = [event_to_convert]

        for playing_indicator_converter in self._playing_indicator_converter_tuple:
            new_converted_event: list[core_events.SimpleEvent] = []
            for simple_event in converted_event:
                converted_simple_event = playing_indicator_converter.convert(
                    simple_event
                )
                new_converted_event.extend(converted_simple_event)

            converted_event = new_converted_event

        return core_events.SequentialEvent(converted_event)

    def convert(self, event_to_convert: core_events.abc.Event) -> core_events.abc.Event:
        converted_event = self._convert_event(event_to_convert, 0)
        return converted_event
