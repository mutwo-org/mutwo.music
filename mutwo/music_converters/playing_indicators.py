"""Apply :class:`~mutwo.music_parameters.abc.PlayingIndicator` on :class:`~mutwo.core_events.abc.Event`.

"""

import abc
import copy
import itertools
import random
import typing

try:
    import quicktions as fractions  # type: ignore
except ImportError:
    import fractions  # type: ignore

from mutwo import core_converters
from mutwo import core_events
from mutwo import core_parameters
from mutwo import core_utilities
from mutwo import music_converters
from mutwo import music_parameters
from mutwo import music_utilities


__all__ = (
    "PlayingIndicatorConverter",
    "ArpeggioConverter",
    "StacattoConverter",
    "ArticulationConverter",
    "TrillConverter",
    "OptionalConverter",
    "PlayingIndicatorsConverter",
)


class PlayingIndicatorConverter(core_converters.abc.Converter):
    """Abstract base class to apply :class:`~mutwo.music_parameters.abc.PlayingIndicator` on a :class:`~mutwo.core_events.Chronon`.

    :param chronon_to_playing_indicator_collection: Function to extract from a
        :class:`mutwo.core_events.Chronon` a
        :class:`mutwo.music_parameters.PlayingIndicatorCollection`
        object. By default it asks the Event for its
        :attr:`~mutwo.music_events.NoteLike.playing_indicator_collection`
        attribute (because by default :class:`mutwo.music_events.NoteLike`
        objects are expected).
        When using different Event classes than :class:`~mutwo.music_events.NoteLike`
        with a different name for their playing_indicator_collection property, this argument
        should be overridden. If the
        function call raises an :obj:`AttributeError` (e.g. if no playing indicator
        collection can be extracted), mutwo will build a playing indicator collection
        from :const:`~mutwo.music_events.configurations.DEFAULT_PLAYING_INDICATORS_COLLECTION_CLASS`.
    :type chronon_to_playing_indicator_collection: typing.Callable[[core_events.Chronon], music_parameters.PlayingIndicatorCollection], optional

    To write a new PlayingIndicatorConverter the abstract method
    :func:`_apply_playing_indicator` and the abstract properties
    `playing_indicator_name` and `default_playing_indicator` have
    to be overridden.
    """

    def __init__(
        self,
        chronon_to_playing_indicator_collection: typing.Callable[
            [core_events.Chronon],
            music_parameters.PlayingIndicatorCollection,
        ] = music_converters.ChrononToPlayingIndicatorCollection(),  # type: ignore
    ):
        self._chronon_to_playing_indicator_collection = (
            chronon_to_playing_indicator_collection
        )

    @abc.abstractmethod
    def _apply_playing_indicator(
        self,
        chronon_to_convert: core_events.Chronon,
        playing_indicator: music_parameters.abc.PlayingIndicator,
    ) -> core_events.Consecution[core_events.Chronon]:
        ...

    @property
    @abc.abstractmethod
    def playing_indicator_name(self) -> str:
        ...

    @property
    @abc.abstractmethod
    def default_playing_indicator(self) -> music_parameters.abc.PlayingIndicator:
        ...

    def convert(
        self, chronon_to_convert: core_events.Chronon
    ) -> core_events.Consecution[core_events.Chronon]:
        """Apply PlayingIndicator on chronon.

        :param chronon_to_convert: The event which shall be converted.
        :type chronon_to_convert: core_events.Chronon
        """

        playing_indicator_collection = self._chronon_to_playing_indicator_collection(
            chronon_to_convert,
        )
        playing_indicator = core_utilities.call_function_except_attribute_error(
            lambda playing_indicator_collection: getattr(
                playing_indicator_collection, self.playing_indicator_name
            ),
            playing_indicator_collection,
            self.default_playing_indicator,
        )

        if playing_indicator.is_active:
            return self._apply_playing_indicator(chronon_to_convert, playing_indicator)
        else:
            return core_events.Consecution([copy.deepcopy(chronon_to_convert)])


class ArpeggioConverter(PlayingIndicatorConverter):
    """Apply arpeggio on :class:`~mutwo.core_events.Chronon`.

    :param duration_for_each_attack: Set how long each attack of the
        Arpeggio lasts. Default to 0.1.
    :type duration_for_each_attack: core_parameters.abc.Duration.Type
    :param chronon_to_pitch_list: Function to extract from a
        :class:`mutwo.core_events.Chronon` a tuple that contains pitch objects
        (objects that inherit from :class:`mutwo.music_parameters.abc.Pitch`).
        By default it asks the Event for its
        :attr:`~mutwo.music_events.NoteLike.pitch_list` attribute
        (because by default :class:`mutwo.music_events.NoteLike` objects are expected).
        When using different Event classes than :class:`~mutwo.music_events.NoteLike`
        with a different name for their pitch property, this argument
        should be overridden.
        If the function call raises an :obj:`AttributeError` (e.g. if no pitch can be
        extracted), mutwo will assume an event without any pitches.
    :type chronon_to_pitch_list: typing.Callable[[core_events.Chronon], music_parameters.abc.Pitch], optional
    :param chronon_to_playing_indicator_collection: Function to extract from a
        :class:`mutwo.core_events.Chronon` a
        :class:`mutwo.music_parameters.PlayingIndicatorCollection`
        object. By default it asks the Event for its
        :attr:`~mutwo.music_events.NoteLike.playing_indicator_collection`
        attribute (because by default :class:`mutwo.music_events.NoteLike`
        objects are expected).
        When using different Event classes than :class:`~mutwo.music_events.NoteLike`
        with a different name for their playing_indicator_collection property, this argument
        should be overridden. If the
        function call raises an :obj:`AttributeError` (e.g. if no playing indicator
        collection can be extracted), mutwo will build a playing indicator collection
        from :const:`~mutwo.music_events.configurations.DEFAULT_PLAYING_INDICATORS_COLLECTION_CLASS`.
    :type chronon_to_playing_indicator_collection: typing.Callable[[core_events.Chronon], music_parameters.PlayingIndicatorCollection,], optional
    :param set_pitch_list_for_chronon: Function which assigns
        a list of :class:`~mutwo.music_parameters.abc.Pitch` objects to a
        :class:`~mutwo.core_events.Chronon`. By default the
        function assigns the passed pitches to the
        :attr:`~mutwo.music_events.NoteLike.pitch_list` attribute
        (because by default :class:`mutwo.music_events.NoteLike` objects
        are expected).
    :type set_pitch_list_for_chronon: typing.Callable[[core_events.Chronon, list[music_parameters.abc.Pitch]], None]
    """

    def __init__(
        self,
        duration_for_each_attack: core_parameters.abc.Duration.Type = 0.1,
        chronon_to_pitch_list: typing.Callable[
            [core_events.Chronon], list[music_parameters.abc.Pitch]
        ] = music_converters.ChrononToPitchList(),
        chronon_to_playing_indicator_collection: typing.Callable[
            [core_events.Chronon],
            music_parameters.PlayingIndicatorCollection,
        ] = music_converters.ChrononToPlayingIndicatorCollection(),
        set_pitch_list_for_chronon: typing.Callable[
            [core_events.Chronon, list[music_parameters.abc.Pitch]], None
        ] = lambda chronon, pitch_list: chronon.set_parameter(  # type: ignore
            "pitch_list", pitch_list, set_unassigned_parameter=True
        ),
    ):
        super().__init__(
            chronon_to_playing_indicator_collection=chronon_to_playing_indicator_collection
        )
        self._duration_for_each_attack = core_parameters.abc.Duration.from_any(
            duration_for_each_attack
        )
        self._chronon_to_pitch_list = chronon_to_pitch_list
        self._set_pitch_list_for_chronon = set_pitch_list_for_chronon

    @property
    def playing_indicator_name(self) -> str:
        return "arpeggio"

    @property
    def default_playing_indicator(self) -> music_parameters.abc.PlayingIndicator:
        return music_parameters.Arpeggio()

    def _apply_playing_indicator(
        self,
        chronon_to_convert: core_events.Chronon,
        playing_indicator: music_parameters.Arpeggio,
    ) -> core_events.Consecution[core_events.Chronon]:
        pitch_list = list(self._chronon_to_pitch_list(chronon_to_convert))

        # sort pitches according to Arpeggio direction
        pitch_list.sort(reverse=playing_indicator.direction != "up")

        converted_event: core_events.Consecution[
            core_events.Chronon
        ] = core_events.Consecution([copy.copy(chronon_to_convert) for _ in pitch_list])

        # apply pitches on events
        for event_index, pitch in enumerate(pitch_list):
            self._set_pitch_list_for_chronon(converted_event[event_index], [pitch])

        # set correct duration for each event
        event_count = len(converted_event)
        duration_of_each_attack = self._duration_for_each_attack
        if duration_of_each_attack * event_count > chronon_to_convert.duration:
            duration_of_each_attack = chronon_to_convert.duration / event_count

        for event_index in range(event_count - 1):
            converted_event[event_index].duration = duration_of_each_attack

        converted_event[-1].duration -= (
            converted_event.duration - chronon_to_convert.duration
        )

        return converted_event


class StacattoConverter(PlayingIndicatorConverter):
    """Apply staccato on :class:`~mutwo.core_events.Chronon`.

    :param factor:
    :param allowed_articulation_name_sequence:
    :param chronon_to_playing_indicator_collection: Function to extract from a
        :class:`mutwo.core_events.Chronon` a
        :class:`mutwo.music_parameters.PlayingIndicatorCollection`
        object. By default it asks the Event for its
        :attr:`~mutwo.music_events.NoteLike.playing_indicator_collection`
        attribute (because by default :class:`mutwo.music_events.NoteLike`
        objects are expected).
        When using different Event classes than :class:`~mutwo.music_events.NoteLike`
        with a different name for their playing_indicator_collection property, this argument
        should be overridden. If the
        function call raises an :obj:`AttributeError` (e.g. if no playing indicator
        collection can be extracted), mutwo will build a playing indicator collection
        from :const:`~mutwo.music_events.configurations.DEFAULT_PLAYING_INDICATORS_COLLECTION_CLASS`.
    :type chronon_to_playing_indicator_collection: typing.Callable[[core_events.Chronon], music_parameters.PlayingIndicatorCollection,], optional
    """

    def __init__(
        self,
        factor: float = 0.5,
        allowed_articulation_name_sequence: typing.Sequence[str] = ("staccato", "."),
        chronon_to_playing_indicator_collection: typing.Callable[
            [core_events.Chronon],
            music_parameters.PlayingIndicatorCollection,
        ] = music_converters.ChrononToPlayingIndicatorCollection(),
    ):
        self._allowed_articulation_name_sequence = allowed_articulation_name_sequence
        self._factor = factor
        super().__init__(chronon_to_playing_indicator_collection)

    def _apply_playing_indicator(
        self,
        chronon_to_convert: core_events.Chronon,
        _: music_parameters.abc.PlayingIndicator,
    ) -> core_events.Consecution[core_events.Chronon]:
        duration = chronon_to_convert.duration * self._factor
        consecution = core_events.Consecution(
            [
                chronon_to_convert.copy().set_parameter("duration", duration),
                core_events.Chronon(duration),
            ]
        )
        return consecution

    @property
    def playing_indicator_name(self) -> str:
        return "articulation"

    @property
    def default_playing_indicator(self) -> music_parameters.abc.PlayingIndicator:
        return music_parameters.Articulation()


class ArticulationConverter(PlayingIndicatorConverter):
    """Apply articulation on :class:`~mutwo.core_events.Chronon`.

    :param articulation_name_tuple_to_playing_indicator_converter:
    :type articulation_name_tuple_to_playing_indicator_converter: dict[tuple[str, ...], PlayingIndicatorConverter]
    :param chronon_to_playing_indicator_collection: Function to extract from a
        :class:`mutwo.core_events.Chronon` a
        :class:`mutwo.music_parameters.PlayingIndicatorCollection`
        object. By default it asks the Event for its
        :attr:`~mutwo.music_events.NoteLike.playing_indicator_collection`
        attribute (because by default :class:`mutwo.music_events.NoteLike`
        objects are expected).
        When using different Event classes than :class:`~mutwo.music_events.NoteLike`
        with a different name for their playing_indicator_collection property, this argument
        should be overridden. If the
        function call raises an :obj:`AttributeError` (e.g. if no playing indicator
        collection can be extracted), mutwo will build a playing indicator collection
        from :const:`~mutwo.music_events.configurations.DEFAULT_PLAYING_INDICATORS_COLLECTION_CLASS`.
    :type chronon_to_playing_indicator_collection: typing.Callable[[core_events.Chronon], music_parameters.PlayingIndicatorCollection,], optional
    """

    def __init__(
        self,
        articulation_name_tuple_to_playing_indicator_converter: dict[
            tuple[str, ...], PlayingIndicatorConverter
        ] = {("staccato", "."): StacattoConverter()},
        chronon_to_playing_indicator_collection: typing.Callable[
            [core_events.Chronon],
            music_parameters.PlayingIndicatorCollection,
        ] = music_converters.ChrononToPlayingIndicatorCollection(),
    ):
        articulation_name_to_playing_indicator_converter = {}
        for (
            articulation_name_tuple,
            playing_indicator_converter,
        ) in articulation_name_tuple_to_playing_indicator_converter.items():
            for articulation_name in articulation_name_tuple:
                if (
                    articulation_name
                    not in articulation_name_to_playing_indicator_converter
                ):
                    self._logger.warning(
                        music_utilities.DuplicatePlayingIndicatorConverterMappingWarning(
                            articulation_name, playing_indicator_converter
                        )
                    )
                articulation_name_to_playing_indicator_converter.update(
                    {articulation_name: playing_indicator_converter}
                )

        self._articulation_name_to_playing_indicator_converter = (
            articulation_name_to_playing_indicator_converter
        )
        super().__init__(chronon_to_playing_indicator_collection)

    def _apply_playing_indicator(
        self,
        chronon_to_convert: core_events.Chronon,
        playing_indicator: music_parameters.Articulation,
    ) -> core_events.Consecution[core_events.Chronon]:
        if (
            playing_indicator.name
            in self._articulation_name_to_playing_indicator_converter
        ):
            return self._articulation_name_to_playing_indicator_converter[
                playing_indicator.name
            ].convert(chronon_to_convert)
        else:
            return core_events.Consecution([copy.deepcopy(chronon_to_convert)])

    @property
    def playing_indicator_name(self) -> str:
        return "articulation"

    @property
    def default_playing_indicator(self) -> music_parameters.abc.PlayingIndicator:
        return music_parameters.Articulation()


class TrillConverter(PlayingIndicatorConverter):
    """Apply trill on :class:`~mutwo.core_events.Chronon`.

    :param trill_size:
    :type trill_size: core_parameters.abc.Duration.Type
    :param chronon_to_pitch_list: Function to extract from a
        :class:`mutwo.core_events.Chronon` a tuple that contains pitch objects
        (objects that inherit from :class:`mutwo.music_parameters.abc.Pitch`).
        By default it asks the Event for its
        :attr:`~mutwo.music_events.NoteLike.pitch_list` attribute
        (because by default :class:`mutwo.music_events.NoteLike` objects are expected).
        When using different Event classes than :class:`~mutwo.music_events.NoteLike`
        with a different name for their pitch property, this argument
        should be overridden.
        If the function call raises an :obj:`AttributeError` (e.g. if no pitch can be
        extracted), mutwo will assume an event without any pitches.
    :type chronon_to_pitch_list: typing.Callable[[core_events.Chronon], music_parameters.abc.Pitch], optional
    :param chronon_to_playing_indicator_collection: Function to extract from a
        :class:`mutwo.core_events.Chronon` a
        :class:`mutwo.music_parameters.PlayingIndicatorCollection`
        object. By default it asks the Event for its
        :attr:`~mutwo.music_events.NoteLike.playing_indicator_collection`
        attribute (because by default :class:`mutwo.music_events.NoteLike`
        objects are expected).
        When using different Event classes than :class:`~mutwo.music_events.NoteLike`
        with a different name for their playing_indicator_collection property, this argument
        should be overridden. If the
        function call raises an :obj:`AttributeError` (e.g. if no playing indicator
        collection can be extracted), mutwo will build a playing indicator collection
        from :const:`~mutwo.music_events.configurations.DEFAULT_PLAYING_INDICATORS_COLLECTION_CLASS`.
    :type chronon_to_playing_indicator_collection: typing.Callable[[core_events.Chronon], music_parameters.PlayingIndicatorCollection,], optional
    """

    def __init__(
        self,
        trill_size: core_parameters.abc.Duration.Type = fractions.Fraction(1, 16),
        chronon_to_pitch_list: typing.Callable[
            [core_events.Chronon], list[music_parameters.abc.Pitch]
        ] = music_converters.ChrononToPitchList(),
        chronon_to_playing_indicator_collection: typing.Callable[
            [core_events.Chronon],
            music_parameters.PlayingIndicatorCollection,
        ] = music_converters.ChrononToPlayingIndicatorCollection(),
    ):
        self._trill_size = core_parameters.abc.Duration.from_any(trill_size)
        self._chronon_to_pitch_list = chronon_to_pitch_list
        super().__init__(chronon_to_playing_indicator_collection)

    def _apply_trill(
        self,
        chronon_to_convert: core_events.Chronon,
        trill: music_parameters.Trill,
        pitch_list: list[music_parameters.abc.Pitch],
    ) -> core_events.Consecution[core_events.Chronon]:
        trill_item_count = chronon_to_convert.duration // self._trill_size
        remaining = chronon_to_convert.duration - (trill_item_count * self._trill_size)
        consecution = core_events.Consecution([])
        pitch_cycle = itertools.cycle((pitch_list, trill.pitch))
        for _ in range(int(trill_item_count)):
            chronon = (
                chronon_to_convert.copy()
                .set_parameter("duration", self._trill_size)
                .set_parameter("pitch_list", next(pitch_cycle))
            )
            consecution.append(chronon)
        consecution[-1].duration += remaining
        return consecution

    def _apply_playing_indicator(
        self,
        chronon_to_convert: core_events.Chronon,
        playing_indicator: music_parameters.Trill,
    ) -> core_events.Consecution[core_events.Chronon]:
        pitch_list = self._chronon_to_pitch_list(chronon_to_convert)
        if pitch_list:
            return self._apply_trill(chronon_to_convert, playing_indicator, pitch_list)
        else:
            return core_events.Consecution([copy.copy(chronon_to_convert)])

    @property
    def playing_indicator_name(self) -> str:
        return "trill"

    @property
    def default_playing_indicator(self) -> music_parameters.abc.PlayingIndicator:
        return music_parameters.Trill()


class OptionalConverter(PlayingIndicatorConverter):
    """Apply optional on :class:`~mutwo.core_events.Chronon`.

    :param likelihood: A number between 0 - 1. 1 means that each optional
        note is played, 0 means no optional note is played. Default to 0.5.
    :type likelihood: float
    :param random_seed: Set inner random process. Default to 100.
    :type random_seed: int
    :param make_rest: A function which takes the original :class:`~mutwo.core_events.Chronon`
        and returns a new `Chronon` with the same duration which represents a rest.
        By default, `mutwo` simply creates a `Chronon` with the same duration.
    :type make_rest: typing.Callable[[core_events.Chronon], core_events.Chronon]
    :param chronon_to_playing_indicator_collection: Function to extract from a
        :class:`mutwo.core_events.Chronon` a
        :class:`mutwo.music_parameters.PlayingIndicatorCollection`
        object. By default it asks the Event for its
        :attr:`~mutwo.music_events.NoteLike.playing_indicator_collection`
        attribute (because by default :class:`mutwo.music_events.NoteLike`
        objects are expected).
        When using different Event classes than :class:`~mutwo.music_events.NoteLike`
        with a different name for their playing_indicator_collection property, this argument
        should be overridden. If the
        function call raises an :obj:`AttributeError` (e.g. if no playing indicator
        collection can be extracted), mutwo will build a playing indicator collection
        from :const:`~mutwo.music_events.configurations.DEFAULT_PLAYING_INDICATORS_COLLECTION_CLASS`.
    :type chronon_to_playing_indicator_collection: typing.Callable[[core_events.Chronon], music_parameters.PlayingIndicatorCollection,], optional
    """

    def __init__(
        self,
        likelihood: float = 0.5,
        random_seed: int = 100,
        make_rest: typing.Callable[
            [core_events.Chronon], core_events.Chronon
        ] = lambda chronon: core_events.Chronon(chronon.duration),
        chronon_to_playing_indicator_collection: typing.Callable[
            [core_events.Chronon],
            music_parameters.PlayingIndicatorCollection,
        ] = music_converters.ChrononToPlayingIndicatorCollection(),
    ):
        self._make_rest = make_rest
        self._likelihood = likelihood
        self._random = random.Random(random_seed)
        super().__init__(chronon_to_playing_indicator_collection)

    def _apply_playing_indicator(
        self,
        chronon_to_convert: core_events.Chronon,
        playing_indicator: music_parameters.abc.ExplicitPlayingIndicator,
    ) -> core_events.Consecution[core_events.Chronon]:
        consecution = core_events.Consecution([])
        if playing_indicator.is_active and self._random.random() > self._likelihood:
            rest = self._make_rest(chronon_to_convert)
            consecution.append(rest)
        else:
            consecution.append(chronon_to_convert.copy())
        return consecution

    @property
    def playing_indicator_name(self) -> str:
        return "optional"

    @property
    def default_playing_indicator(self) -> music_parameters.abc.PlayingIndicator:
        return music_parameters.abc.ExplicitPlayingIndicator()


class PlayingIndicatorsConverter(core_converters.abc.SymmetricalEventConverter):
    """Apply :class:`mutwo.music_parameters.abc.PlayingIndicator` on any :class:`~mutwo.core_events.abc.Event`.

    :param playing_indicator_converter_sequence: A sequence of :class:`PlayingIndicatorConverter` which shall
        be applied on each :class:`~mutwo.core_events.Chronon`.
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

    def _convert_chronon(
        self,
        event_to_convert: core_events.Chronon,
        _: core_parameters.abc.Duration.Type,
    ) -> core_events.Consecution:
        """Convert instance of :class:`mutwo.core_events.Chronon`."""

        converted_event = [event_to_convert]

        for playing_indicator_converter in self._playing_indicator_converter_tuple:
            new_converted_event: list[core_events.Chronon] = []
            for chronon in converted_event:
                converted_chronon = playing_indicator_converter.convert(chronon)
                new_converted_event.extend(converted_chronon)

            converted_event = new_converted_event

        return core_events.Consecution(converted_event)

    def convert(self, event_to_convert: core_events.abc.Event) -> core_events.abc.Event:
        converted_event = self._convert_event(event_to_convert, 0)
        return converted_event
