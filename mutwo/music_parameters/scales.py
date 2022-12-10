"""Write musical scales e.g. minor scale, pelog scale.

The mutwo scale model is influenced by the music21 scale model.
"""

import functools
import operator
import typing

from mutwo import core_constants
from mutwo import core_utilities
from mutwo import music_parameters
from mutwo import music_utilities

__all__ = ("ScaleFamily", "RepeatingScaleFamily", "Scale")


IntervalSequence: typing.TypeAlias = typing.Sequence[music_parameters.abc.PitchInterval]
WeightSequence: typing.TypeAlias = typing.Sequence[core_constants.Real]

IntervalTuple: typing.TypeAlias = tuple[music_parameters.abc.PitchInterval, ...]
WeightTuple: typing.TypeAlias = tuple[core_constants.Real, ...]

PitchTuple: typing.TypeAlias = tuple[music_parameters.abc.Pitch, ...]

ScaleDegree: typing.TypeAlias = int
ScaleIndex: typing.TypeAlias = int

PeriodRepetitionCount: typing.TypeAlias = int
"""How often the repeating interval has been applied (e.g. the octave)."""

ScalePosition: typing.TypeAlias = tuple[ScaleDegree, PeriodRepetitionCount]

PeriodRepetitionCountTuple: typing.TypeAlias = tuple[PeriodRepetitionCount, ...]
ScaleDegreeTuple: typing.TypeAlias = tuple[ScaleDegree, ...]
ScaleDegreeSequence: typing.TypeAlias = typing.Sequence[ScaleDegree]
PeriodRepetitionCountSequence: typing.TypeAlias = typing.Sequence[PeriodRepetitionCount]


class ScaleFamily(object):
    """A :class:`ScaleFamily` is a sorted sequence of :class:`~mutwo.music_parameters.abc.PitchInterval`s.

    Scale families are frozen/immutable.

    The equivalent of a `ScaleFamily` in `music21` is an `AbstractScale`.

    `Mutwos` implementation supports assigning weights to each interval
    to express an hierarchy within the scale.

    You need to explicitly add the prime (1/1) to the interval set
    if the tonic should appear within the given scale.
    """

    def __init__(
        self,
        interval_sequence: IntervalSequence,
        weight_sequence: typing.Optional[WeightSequence] = None,
        scale_degree_sequence: typing.Optional[ScaleDegreeSequence] = None,
        period_repetition_count_sequence: typing.Optional[
            PeriodRepetitionCountSequence
        ] = None,
    ):
        interval_tuple = tuple(interval_sequence)

        weight_tuple = ScaleFamily._weight_sequence_to_weight_tuple(
            weight_sequence, interval_tuple
        )
        scale_degree_tuple = ScaleFamily._scale_degree_sequence_to_scale_tuple(
            scale_degree_sequence, interval_tuple
        )
        period_repetition_count_tuple = ScaleFamily._period_repetition_count_sequence_to_period_repetition_count_tuple(
            period_repetition_count_sequence, interval_tuple
        )

        is_rising = ScaleFamily._is_interval_tuple_rising(interval_tuple)

        self._interval_tuple = interval_tuple
        self._weight_tuple = weight_tuple
        self._scale_degree_tuple = scale_degree_tuple
        self._period_repetition_count_tuple = period_repetition_count_tuple
        self._is_rising = is_rising

    def __eq__(self, other: typing.Any) -> bool:
        return core_utilities.test_if_objects_are_equal_by_parameter_tuple(
            self, other, ("interval_tuple", "weight_tuple")
        )

    @staticmethod
    def _sequence_to_tuple(
        sequence: typing.Optional[typing.Sequence[typing.Any]],
        interval_tuple: IntervalTuple,
        auto_create_tuple: typing.Callable[[IntervalTuple], tuple[typing.Any, ...]],
        item_name: str,
    ) -> tuple[core_constants.Real, ...]:
        sequence = sequence or auto_create_tuple(interval_tuple)
        tuple_ = tuple(sequence)

        assert len(tuple_) == len(
            interval_tuple
        ), f"We need as many {item_name} entries as there are interval entries!"

        return tuple_

    @staticmethod
    def _scale_degree_sequence_to_scale_tuple(
        scale_degree_sequence: typing.Optional[ScaleDegreeSequence],
        interval_tuple: IntervalTuple,
    ) -> ScaleDegreeTuple:
        return ScaleFamily._sequence_to_tuple(
            scale_degree_sequence,
            interval_tuple,
            lambda interval_tuple: tuple(range(len(interval_tuple))),
            "interval",
        )

    @staticmethod
    def _weight_sequence_to_weight_tuple(
        weight_sequence: typing.Optional[WeightSequence], interval_tuple: IntervalTuple
    ) -> tuple[core_constants.Real, ...]:
        return ScaleFamily._sequence_to_tuple(
            weight_sequence,
            interval_tuple,
            lambda interval_tuple: tuple(1 for _ in interval_tuple),
            "weight",
        )

    @staticmethod
    def _period_repetition_count_sequence_to_period_repetition_count_tuple(
        period_repetition_count_sequence: typing.Optional[
            PeriodRepetitionCountSequence
        ],
        interval_tuple: IntervalTuple,
    ) -> tuple[core_constants.Real, ...]:
        return ScaleFamily._sequence_to_tuple(
            period_repetition_count_sequence,
            interval_tuple,
            lambda interval_tuple: tuple(0 for _ in interval_tuple),
            "period repetition count",
        )

    @staticmethod
    def _is_interval_tuple_rising(interval_tuple: IntervalTuple) -> bool:
        rising_interval_tuple, falling_interval_tuple = (
            tuple(sorted(interval_tuple, reverse=reverse)) for reverse in (False, True)
        )
        is_rising = interval_tuple == rising_interval_tuple
        if not is_rising and interval_tuple != falling_interval_tuple:
            raise music_utilities.UnsortedIntervalTupleError(interval_tuple)
        return is_rising

    @property
    def interval_tuple(self) -> IntervalTuple:
        return self._interval_tuple

    @property
    def weight_tuple(self) -> WeightTuple:
        return self._weight_tuple

    @property
    def scale_degree_tuple(self) -> ScaleDegreeTuple:
        return self._scale_degree_tuple

    @property
    def period_repetition_count_tuple(self) -> PeriodRepetitionCountTuple:
        return self._period_repetition_count_tuple

    @property
    def is_rising(self) -> bool:
        return self._is_rising

    @functools.cached_property
    def is_falling(self) -> bool:
        return not self.is_rising


class RepeatingScaleFamily(ScaleFamily):
    """A `RepeatingScaleFamily` is a sorted sequence of repeating intervals over a repetition interval.

    Most musical scales are based on :class:`RepeatingScaleFamily`, because
    most musical scales repeat after one octave.
    """

    def __init__(
        self,
        repeating_interval_sequence: IntervalSequence,
        repetition_interval: music_parameters.abc.PitchInterval = music_parameters.DirectPitchInterval(
            1200
        ),
        min_pitch_interval: music_parameters.abc.PitchInterval = music_parameters.DirectPitchInterval(
            -1200 * 5
        ),
        max_pitch_interval: music_parameters.abc.PitchInterval = music_parameters.DirectPitchInterval(
            1200 * 5
        ),
        repeating_weight_sequence: typing.Optional[WeightSequence] = None,
        repeating_scale_degree_sequence: typing.Optional[ScaleDegreeSequence] = None,
        repeating_period_repetition_count_sequence: typing.Optional[
            PeriodRepetitionCountSequence
        ] = None,
    ):
        # TODO(Make this somehow readable.)
        repeating_interval_tuple = tuple(repeating_interval_sequence)
        repeating_weight_tuple = ScaleFamily._weight_sequence_to_weight_tuple(
            repeating_weight_sequence, repeating_interval_tuple
        )
        repeating_scale_degree_tuple = (
            ScaleFamily._scale_degree_sequence_to_scale_tuple(
                repeating_scale_degree_sequence, repeating_interval_tuple
            )
        )
        repeating_period_repetition_count_tuple = ScaleFamily._period_repetition_count_sequence_to_period_repetition_count_tuple(
            repeating_period_repetition_count_sequence, repeating_interval_tuple
        )

        is_rising = ScaleFamily._is_interval_tuple_rising(repeating_interval_tuple)

        interval_range = (
            repeating_interval_tuple[0].interval - repeating_interval_tuple[-1].interval
        )

        assert abs(interval_range) < abs(repetition_interval.interval), (
            "Repetition interval has to be bigger than "
            "ambitus of repeating interval sequence!"
        )

        interval_data_list = [
            (interval, weight, scale_degree, period_repetition_count)
            for interval, weight, scale_degree, period_repetition_count in zip(
                repeating_interval_tuple,
                repeating_weight_tuple,
                repeating_scale_degree_tuple,
                repeating_period_repetition_count_tuple,
            )
            if interval >= min_pitch_interval and interval < max_pitch_interval
        ]

        for local_repetition_interval in (
            repetition_interval,
            repetition_interval.inverse(mutate=False),
        ):
            last_interval_data_list = list(
                zip(
                    repeating_interval_tuple,
                    repeating_weight_tuple,
                    repeating_scale_degree_tuple,
                    repeating_period_repetition_count_tuple,
                )
            )
            if local_repetition_interval.interval > 0:
                period_repetition_delta = 1
            else:
                period_repetition_delta = -1
            while 1:
                new_interval_data_list = []
                is_valid = True
                for (
                    interval,
                    weight,
                    scale_degree,
                    period_repetition_count,
                ) in last_interval_data_list:
                    if (
                        (new_interval := interval + local_repetition_interval)
                        < max_pitch_interval
                    ) and (new_interval >= min_pitch_interval):
                        new_interval_data_list.append(
                            (
                                new_interval,
                                weight,
                                scale_degree,
                                period_repetition_count + period_repetition_delta,
                            )
                        )
                    else:
                        is_valid = False
                interval_data_list.extend(new_interval_data_list)
                if not is_valid:
                    break
                last_interval_data_list = new_interval_data_list

        interval_data_list.sort(key=operator.itemgetter(0), reverse=not is_rising)

        super().__init__(*zip(*interval_data_list))


class Scale(object):
    """A :class:`Scale` is a sorted sequence of :class:`~mutwo.music_parameters.abc.Pitch`es.

    The equivalent of a `Scale` in `music21` is an `ConcreteScale`.

    :class:`Scale` uses a specific nomenclature to differentiate between
    different positions in a musical scale:

        1. `scale_degree`: A scale degree is an octave independent position of
           a :class:`~mutwo.music_parameters.abc.Pitch`.

        2. `scale_index`: A scale index is an absolute index of a
           :class:`~mutwo.music_parameters.abc.Pitch` within a
           specific scale.
    """

    def __init__(self, tonic: music_parameters.abc.Pitch, scale_family: ScaleFamily):
        self.tonic = tonic
        self.scale_family = scale_family

    # ###################################################################### #
    #                           magic methods                                #
    # ###################################################################### #

    def __contains__(self, item: typing.Any) -> bool:
        return item in self.pitch_tuple

    def __eq__(self, other: typing.Any) -> bool:
        return core_utilities.test_if_objects_are_equal_by_parameter_tuple(
            self, other, ("tonic", "scale_family")
        )

    # ###################################################################### #
    #                           private methods                              #
    # ###################################################################### #

    def _reset(self):
        for property_name in ("pitch_tuple", "scale_position_tuple"):
            try:
                delattr(self, property_name)
            except AttributeError:
                pass

    # ###################################################################### #
    #                           public properties                            #
    # ###################################################################### #

    @property
    def tonic(self) -> music_parameters.abc.Pitch:
        return self._tonic

    @tonic.setter
    def tonic(self, tonic: music_parameters.abc.Pitch):
        self._tonic = tonic
        self._reset()

    @property
    def scale_family(self) -> ScaleFamily:
        return self._scale_family

    @scale_family.setter
    def scale_family(self, scale_family: ScaleFamily):
        self._scale_family = scale_family
        self._reset()

    @functools.cached_property
    def pitch_tuple(self) -> PitchTuple:
        return tuple(
            self.tonic + interval for interval in self.scale_family.interval_tuple
        )

    @property
    def weight_tuple(self) -> WeightTuple:
        return self.scale_family.weight_tuple

    @property
    def scale_degree_tuple(self) -> ScaleDegreeTuple:
        return self.scale_family.scale_degree_tuple

    @property
    def period_repetition_count_tuple(self) -> PeriodRepetitionCountTuple:
        return self.scale_family.period_repetition_count_tuple

    @functools.cached_property
    def scale_position_tuple(self) -> tuple[ScalePosition, ...]:
        return tuple(zip(self.scale_degree_tuple, self.period_repetition_count_tuple))

    @property
    def is_rising(self) -> bool:
        return self.scale_family.is_rising

    @property
    def is_falling(self) -> bool:
        return self.scale_family.is_falling

    # ###################################################################### #
    #                           public methods                               #
    # ###################################################################### #

    def pitch_to_scale_degree(self, pitch: music_parameters.abc.Pitch) -> ScaleDegree:
        return self.scale_degree_tuple[self.pitch_tuple.index(pitch)]

    def scale_position_to_pitch(
        self, scale_position: ScalePosition
    ) -> music_parameters.abc.Pitch:
        return self.pitch_tuple[self.scale_position_tuple.index(scale_position)]

    def pitch_to_scale_position(
        self, pitch: music_parameters.abc.Pitch
    ) -> music_parameters.abc.Pitch:
        return self.scale_position_tuple[self.pitch_tuple.index(pitch)]

    def pitch_to_scale_index(self, pitch: music_parameters.abc.Pitch) -> ScaleIndex:
        return self.pitch_tuple.index(pitch)

    def scale_index_to_pitch(
        self, scale_index: ScaleIndex
    ) -> music_parameters.abc.Pitch:
        return self.pitch_tuple[scale_index]
