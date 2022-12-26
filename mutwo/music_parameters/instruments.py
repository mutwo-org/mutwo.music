"""Representations for musical instruments"""

from __future__ import annotations

import collections
import functools
import itertools
import typing

from ortools.sat.python import cp_model

from mutwo import core_utilities
from mutwo import music_parameters


__all__ = (
    "UnpitchedInstrument",
    "ContinuousPitchedInstrument",
    "DiscreetPitchedInstrument",
    "Orchestration",
    "OrchestrationMixin",
    "CelticHarp",
    "Piccolo",
    "Flute",
    "Oboe",
    "BfClarinet",
    "EfClarinet",
    "Bassoon",
)


class UnpitchedInstrument(music_parameters.abc.Instrument):
    """Model a musical instruments without any clear pitches.

    **Example:**

    >>> from mutwo import music_parameters
    >>> bass_drum = music_parameters.UnpitchedInstrument("bass drum", "bd.")
    """

    @property
    def is_pitched(self) -> bool:
        return False


class ContinuousPitchedInstrument(music_parameters.abc.PitchedInstrument):
    """Model a musical instrument with continuous pitches (e.g. not fretted).

    :param pitch_ambitus: The pitch ambitus of the instrument.
    :type pitch_ambitus: music_parameters.abc.PitchAmbitus
    :param name: The name of the instrument.
    :type name: str
    :param short_name: The abbreviation of the instrument.
        If set to ``None`` it will be the same like `name`.
        Default to ``None``.
    :type short_name: typing.Optional[str]
    :param pitch_count_range: Set how many simultaneous
        pitches the instrument can play. Default to
        `ranges.Range(1, 2)`, which means that the instrument
        is monophonic.
    :type pitch_count_range: ranges.Range
    :param transposition_pitch_interval: Some instruments are
        written with a transposition (so sounding pitch and
        written pitch differs). This parameter can be used
        to set the transposition interval in case sounding
        and written differs. The `transposition_pitch_interval`
        is added to the sounding pitches in order to reach the
        written pitches. If set to ``None`` this will be
        set to `DirectPitchInterval(0)` which is no transposition.
        Default to ``None``.
    :type transposition_pitch_interval: typing.Optional[PitchInterval]

    **Example:**

    >>> from mutwo import music_parameters
    >>> vl = music_parameters.ContinuousPitchedInstrument(
    ...     music_parameters.OctaveAmbitus(
    ...         music_parameters.WesternPitch('g', 3),
    ...         music_parameters.WesternPitch('e', 7),
    ...     ),
    ...     "violin",
    ...     "vl.",
    ... )
    """

    def __init__(
        self, pitch_ambitus: music_parameters.abc.PitchAmbitus, *args, **kwargs
    ):
        super().__init__(*args, **kwargs)
        self._pitch_ambitus = pitch_ambitus

    def __contains__(self, pitch: typing.Any) -> bool:
        """Test if pitch is playable by instrument.

        :param pitch: Pitch to test.
        :type pitch: typing.Any

        **Example:**

        >>> from mutwo import music_parameters
        >>> music_parameters.WesternPitch('c', 1) in music_parameters.BfClarinet()
        False
        """
        return pitch in self.pitch_ambitus

    @property
    def pitch_ambitus(self) -> music_parameters.abc.PitchAmbitus:
        return self._pitch_ambitus


class DiscreetPitchedInstrument(music_parameters.abc.PitchedInstrument):
    """Model a musical instrument with discreet pitches (e.g. fretted).

    :param pitch_tuple: A tuple of all playable pitches of the instrument.
    :type pitch_tuple: tuple[music_parameters.abc.Pitch, ...]
    :param name: The name of the instrument.
    :type name: str
    :param short_name: The abbreviation of the instrument.
        If set to ``None`` it will be the same like `name`.
        Default to ``None``.
    :type short_name: typing.Optional[str]
    :param pitch_count_range: Set how many simultaneous
        pitches the instrument can play. Default to
        `ranges.Range(1, 2)`, which means that the instrument
        is monophonic.
    :type pitch_count_range: ranges.Range
    :param transposition_pitch_interval: Some instruments are
        written with a transposition (so sounding pitch and
        written pitch differs). This parameter can be used
        to set the transposition interval in case sounding
        and written differs. The `transposition_pitch_interval`
        is added to the sounding pitches in order to reach the
        written pitches. If set to ``None`` this will be
        set to `DirectPitchInterval(0)` which is no transposition.
        Default to ``None``.
    :type transposition_pitch_interval: typing.Optional[PitchInterval]

    **Example:**

    >>> from mutwo import music_parameters
    >>> pentatonic_idiophone = music_parameters.DiscreetPitchedInstrument(
    ...     (
    ...         music_parameters.JustIntonationPitch('1/1'),
    ...         music_parameters.JustIntonationPitch('9/8'),
    ...         music_parameters.JustIntonationPitch('5/4'),
    ...         music_parameters.JustIntonationPitch('3/2'),
    ...         music_parameters.JustIntonationPitch('7/4'),
    ...     ),
    ...     "idiophone",
    ...     "id.",
    ... )
    """

    def __init__(
        self, pitch_tuple: tuple[music_parameters.abc.Pitch, ...], *args, **kwargs
    ):
        super().__init__(*args, **kwargs)
        self._pitch_tuple = tuple(sorted(core_utilities.uniqify_sequence(pitch_tuple)))
        self._pitch_ambitus = music_parameters.OctaveAmbitus(
            pitch_tuple[0], pitch_tuple[-1]
        )

    def __contains__(self, pitch: typing.Any) -> bool:
        return pitch in self.pitch_tuple

    @property
    def pitch_ambitus(self) -> music_parameters.abc.PitchAmbitus:
        return self._pitch_ambitus

    @property
    def pitch_tuple(self) -> tuple[music_parameters.abc.Pitch, ...]:
        return self._pitch_tuple


class OrchestrationMixin(object):
    """Helper base class from which adhoc created `Orchestration` object inherits.

    This class has some methods which extend the functionality of
    Pythons builtin `collections.namedtuple`.
    """

    def get_subset(self, *instrument_name: str):
        r"""Return a sub-Orchestration of `Orchestration`.

        :param \*instrument_name: Name of the instrument which should be
            included in the subset.
        :type \*instrument_name: str

        This method doesn't change the original `Orchestration`
        but creates a new object.

        **Example:**

        >>> from mutwo import music_parameters
        >>> orch = music_parameters.Orchestration(
        ...   oboe0=music_parameters.Oboe(),
        ...   oboe1=music_parameters.Oboe(),
        ...   oboe2=music_parameters.Oboe(),
        ... )
        >>> orch.get_subset('oboe0', 'oboe2')
        Orchestration(oboe0=Oboe(name='oboe', short_name='ob.', pitch_count_range=Range[1, 2), transposition_pitch_interval=DirectPitchInterval(interval = 0)), oboe2=Oboe(name='oboe', short_name='ob.', pitch_count_range=Range[1, 2), transposition_pitch_interval=DirectPitchInterval(interval = 0)))
        """
        return Orchestration(**{name: getattr(self, name) for name in instrument_name})


def Orchestration(**instrument_name_to_instrument: music_parameters.abc.Instrument):
    r"""Create a name space for the instrumentation of a composition.

    :param \**instrument_name_to_instrument: Pick any instrument name
        and map it to a specific instrument.
    :type \**instrument_name_to_instrument: music_parameters.abc.Instrument

    This returns an adapted `namedtuple instance <https://docs.python.org/3/library/collections.html#collections.namedtuple>`_
    where the keys are the instrument names and the values are the
    :class:`mutwo.music_parameters.abc.Instrument` objects.
    The returned `Orchestration` object has some additional methods.
    They are documented in the :class`OrchestrationMixin`.

    **Example:**

    >>> from mutwo import music_parameters
    >>> music_parameters.Orchestration(
    ...   oboe0=music_parameters.Oboe(),
    ...   oboe1=music_parameters.Oboe(),
    ... )
    Orchestration(oboe0=Oboe(name='oboe', short_name='ob.', pitch_count_range=Range[1, 2), transposition_pitch_interval=DirectPitchInterval(interval = 0)), oboe1=Oboe(name='oboe', short_name='ob.', pitch_count_range=Range[1, 2), transposition_pitch_interval=DirectPitchInterval(interval = 0)))
    """

    instrument_name_tuple, instrument_tuple = zip(
        *instrument_name_to_instrument.items()
    )

    return type(
        "Orchestration",
        (
            collections.namedtuple("Orchestration", instrument_name_tuple),
            OrchestrationMixin,
        ),
        {},
    )(*instrument_tuple)


class CelticHarp(DiscreetPitchedInstrument):
    """A typical beginners harp without any pedals."""

    def __init__(self, **kwargs):
        super().__init__(
            **_setdefault(
                kwargs, music_parameters.configurations.DEFAULT_CELTIC_HARP_DICT
            )
        )

    class Fingering(music_parameters.abc.Fingering):
        class Vector(collections.namedtuple("Vector", ("string_index",))):
            def __sub__(
                self, other: CelticHarp.Fingering.Vector
            ) -> CelticHarp.Fingering.Vector:
                return type(self)(self.string_index - other.string_index)

        class Part(music_parameters.abc.Fingering.Part):
            class Delta(music_parameters.abc.Fingering.Part.Delta):
                @functools.cached_property
                def score(self) -> float:
                    return 1

    STRING_DISTANCE_TO_FINGER_INDEX_PAIR_TUPLE_DICT = {
        1: ((3, 2), (2, 1)),
        2: ((3, 2), (3, 1), (2, 1), (1, 0)),
    }

    STRING_DISTANCE_TO_FINGER_INDEX_PAIR_TUPLE_DICT = {
        string_distance: tuple((-a, -b) for a, b in finger_index_pair_tuple)
        + finger_index_pair_tuple
        for string_distance, finger_index_pair_tuple in STRING_DISTANCE_TO_FINGER_INDEX_PAIR_TUPLE_DICT.items()
    }

    _joker = tuple(itertools.product(range(-4, 0), range(0, 4)))

    _left_hand = music_parameters.constants.BODY.Left.Arm.Hand.Finger
    _right_hand = music_parameters.constants.BODY.Right.Arm.Hand.Finger

    FINGER_INDEX_TO_FINGER = {
        -1: _left_hand.One,
        -2: _left_hand.Two,
        -3: _left_hand.Three,
        -4: _left_hand.Four,
        0: _right_hand.One,
        1: _right_hand.Two,
        2: _right_hand.Three,
        3: _right_hand.Four,
    }

    def string_distance_to_finger_index_pair_tuple(
        self, string_distance: int
    ) -> tuple[tuple[int, int], ...]:
        # We can't touch anything too far.
        # This doesn't matter if we use two different hands; they
        # can be as far as possible.
        try:
            finger_index_pair_tuple = (
                self.STRING_DISTANCE_TO_FINGER_INDEX_PAIR_TUPLE_DICT[string_distance]
            )
        except KeyError:
            finger_index_pair_tuple = tuple([])
        return finger_index_pair_tuple + self._joker

    def pitch_sequence_to_fingering_tuple(
        self, pitch_sequence: typing.Sequence[music_parameters.abc.Pitch]
    ) -> tuple[CelticHarp.Fingering, ...]:
        pitch_count = len(pitch_sequence)
        assert pitch_count <= 8, "Harp players only use 8 fingers!"

        # Very important!
        pitch_sequence = sorted(pitch_sequence)

        # We already know which strings need to be plucked.
        vector_list = []
        for pitch in pitch_sequence:
            try:
                vector_list.append(self.Fingering.Vector(self.pitch_tuple.index(pitch)))
            except ValueError:
                raise ValueError(f"tuple.index(x): '{pitch}' not in '{self}'")

        model = cp_model.CpModel()

        # Model which fingers we use.
        finger_index_list = []
        for finger_index in range(pitch_count):
            # We use negative domain for left hand and positive
            # domain for right hand.
            finger_index_list.append(
                model.NewIntVarFromDomain(
                    cp_model.Domain.FromIntervals([[-4, -1], [1, 4]]),
                    f"FingerIndex{finger_index}",
                )
            )
        model.AddAllDifferent(finger_index_list)

        # Add hand constraints: We can't touch anything too far.
        for finger_index0, finger_index1 in itertools.combinations(
            range(pitch_count), 2
        ):
            string_distance = (
                vector_list[finger_index1] - vector_list[finger_index0]
            ).string_index
            assert string_distance != 0, "Found two equal pitches!"
            model.AddAllowedAssignments(
                (finger_index_list[finger_index0], finger_index_list[finger_index1]),
                self.string_distance_to_finger_index_pair_tuple(string_distance),
            )

        solver = cp_model.CpSolver()
        solution_collector = _VarArraySolutionCollector(finger_index_list)
        solver.parameters.enumerate_all_solutions = True
        solver.Solve(model, solution_collector)

        fingering_list = []
        for solution in solution_collector.solution_tuple:
            finger_part_list = []
            for pitch, finger_index, vector in zip(
                pitch_sequence, finger_index_list, vector_list
            ):
                finger = self.FINGER_INDEX_TO_FINGER[solution[finger_index.Name()]]
                finger_part_list.append(
                    self.Fingering.Part(finger, frozenset((vector,)), sound=(pitch,))
                )
            fingering_list.append(self.Fingering(finger_part_list))

        return tuple(fingering_list)


class _VarArraySolutionCollector(cp_model.CpSolverSolutionCallback):
    def __init__(self, variables):
        cp_model.CpSolverSolutionCallback.__init__(self)
        self.__variables = variables
        self.__solution_count = 0
        self.__solution_list = []

    def on_solution_callback(self):
        self.__solution_count += 1
        solution_dict = {}
        for v in self.__variables:
            solution_dict[v.Name()] = self.Value(v)
        self.__solution_list.append(solution_dict)

    @property
    def solution_tuple(self) -> tuple[dict, ...]:
        return self.__solution_list


class Piccolo(ContinuousPitchedInstrument):
    def __init__(self, **kwargs):
        super().__init__(
            **_setdefault(kwargs, music_parameters.configurations.DEFAULT_PICCOLO_DICT)
        )


class Flute(ContinuousPitchedInstrument):
    def __init__(self, **kwargs):
        super().__init__(
            **_setdefault(kwargs, music_parameters.configurations.DEFAULT_FLUTE_DICT)
        )


class Oboe(ContinuousPitchedInstrument):
    def __init__(self, **kwargs):
        super().__init__(
            **_setdefault(kwargs, music_parameters.configurations.DEFAULT_OBOE_DICT)
        )


class BfClarinet(ContinuousPitchedInstrument):
    def __init__(self, **kwargs):
        super().__init__(
            **_setdefault(
                kwargs, music_parameters.configurations.DEFAULT_BF_CLARINET_DICT
            )
        )


class EfClarinet(ContinuousPitchedInstrument):
    def __init__(self, **kwargs):
        super().__init__(
            **_setdefault(
                kwargs, music_parameters.configurations.DEFAULT_EF_CLARINET_DICT
            )
        )


class Bassoon(ContinuousPitchedInstrument):
    def __init__(self, **kwargs):
        super().__init__(
            **_setdefault(kwargs, music_parameters.configurations.DEFAULT_BASSOON_DICT)
        )


# Helper
def _setdefault(kwargs: dict, default_dict: dict) -> dict:
    for key, value in default_dict.items():
        kwargs.setdefault(key, value)
    return kwargs
