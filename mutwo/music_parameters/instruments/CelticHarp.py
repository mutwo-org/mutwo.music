from __future__ import annotations

import collections
import functools
import itertools
import typing

import numpy as np

try:
    from ortools.sat.python import cp_model
except ImportError:
    cp_model = None

from mutwo import music_parameters
from mutwo import music_utilities

from .general import DiscreetPitchedInstrument, _setdefault

# Can't be set inside constants due to circular import issues.
left_hand = music_parameters.constants.BODY.Left.Arm.Hand.Finger
right_hand = music_parameters.constants.BODY.Right.Arm.Hand.Finger
h = music_parameters.constants.HarpFinger
music_parameters.constants.HARP_FINGER_INDEX_TO_FINGER = {
    h.LeftOne: left_hand.One,
    h.LeftTwo: left_hand.Two,
    h.LeftThree: left_hand.Three,
    h.LeftFour: left_hand.Four,
    h.RightOne: right_hand.One,
    h.RightTwo: right_hand.Two,
    h.RightThree: right_hand.Three,
    h.RightFour: right_hand.Four,
}
music_parameters.constants.HARP_FINGER_TO_FINGER_INDEX = {
    v: k for k, v in music_parameters.constants.HARP_FINGER_INDEX_TO_FINGER.items()
}
del h, left_hand, right_hand


class CelticHarp(DiscreetPitchedInstrument):
    """A typical beginners harp without any pedals."""

    def __init__(
        self,
        string_distance_to_finger_index_pair_tuple_dict: typing.Optional[
            dict[StringDistance, tuple[FingerIndexPair, ...]]
        ] = None,
        **kwargs,
    ):
        # Arg initialization
        self._string_distance_to_finger_index_pair_tuple_dict = (
            string_distance_to_finger_index_pair_tuple_dict
            or music_parameters.configurations.DEFAULT_STRING_DISTANCE_TO_FINGER_INDEX_PAIR_TUPLE_DICT
        )
        super().__init__(
            **_setdefault(
                kwargs, music_parameters.configurations.DEFAULT_CELTIC_HARP_DICT
            )
        )

    def string_distance_to_finger_index_pair_tuple(
        self, string_distance: int
    ) -> tuple[tuple[int, int], ...]:
        return self._string_distance_to_finger_index_pair_tuple_dict.get(
            string_distance, tuple([])
        )

    def pitch_sequence_to_fingering_tuple(
        self, pitch_sequence: typing.Sequence[music_parameters.abc.Pitch]
    ) -> tuple[CelticHarp.Fingering, ...]:
        if not cp_model:
            raise music_utilities.NotInstalledError(
                "pitch_sequence_to_fingering_tuple", "ortools"
            )

        pitch_count = len(pitch_sequence)
        assert pitch_count <= 8, "Harp players only use 8 fingers!"

        # Very important!
        pitch_sequence = sorted(pitch_sequence)

        # We already know which strings need to be plucked.
        vector_list = [
            self.Fingering.Vector(self.pitch_tuple.index(pitch))
            for pitch in pitch_sequence
        ]
        model = cp_model.CpModel()

        # Model which fingers we use.
        finger_index_list = []
        for finger_index in range(pitch_count):
            finger_index_list.append(
                model.NewIntVarFromDomain(
                    _FINGER_INDEX_DOMAIN, f"FingerIndex{finger_index}"
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

        return self._solution_collector_to_fingering_tuple(
            solution_collector, pitch_sequence, finger_index_list, vector_list
        )

    # Helper method for 'pitch_sequence_to_fingering_tuple'
    def _solution_collector_to_fingering_tuple(
        self,
        solution_collector: _VarArraySolutionCollector,
        pitch_sequence: typing.Sequence[music_parameters.abc.Pitch],
        finger_index_list: list,
        vector_list: list[CelticHarp.Fingering.Vector],
    ) -> tuple[CelticHarp.Fingering, ...]:
        fingering_list = []
        for solution in solution_collector.solution_tuple:
            finger_part_list = []
            for pitch, finger_index, vector in zip(
                pitch_sequence, finger_index_list, vector_list
            ):
                finger = music_parameters.constants.HARP_FINGER_INDEX_TO_FINGER[
                    solution[finger_index.Name()]
                ]
                finger_part_list.append(
                    self.Fingering.Part(finger, frozenset((vector,)), sound=(pitch,))
                )
            fingering_list.append(self.Fingering(finger_part_list))
        return tuple(fingering_list)


A = typing.TypeAlias
FingerIndex: A = int
Score: A = float
StringDistance: A = int
StringDistanceToScoreDict: A = dict[StringDistance, Score]
FingerIndexPair: A = tuple[FingerIndex, FingerIndex]
DeltaScoreMapping: A = dict[FingerIndexPair, StringDistanceToScoreDict]


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
                f2fi = music_parameters.constants.HARP_FINGER_TO_FINGER_INDEX
                string_distance_to_score_dict = (
                    music_parameters.configurations.HARP_DELTA_SCORE_MAPPING[
                        (f2fi[self.body_part_start], f2fi[self.body_part_end])
                    ]
                )
                score_list = []
                for vector in self.vector_set:
                    score_list.append(
                        string_distance_to_score_dict.get(vector.string_index, 0)
                    )
                return float(np.average(score_list))

    # Omit any delta between different hands: they don't matter.
    def delta(
        self, other: CelticHarp.Fingering, distance: int = 1
    ) -> CelticHarp.Fingering.Delta:
        def is_in_same_hand(part_delta: CelticHarp.Part.Delta) -> bool:
            return part_delta.body_part_start.side == part_delta.body_part_end.side

        delta = super().delta(other, distance=distance)
        return self.Delta(
            [part_delta for part_delta in delta if is_in_same_hand(part_delta)],
            distance=distance,
        )


CelticHarp.Fingering = Fingering


if cp_model:

    class _VarArraySolutionCollector(cp_model.CpSolverSolutionCallback):
        def __init__(self, variable_list):
            super().__init__()
            self._variable_list, self._solution_list = variable_list, []

        def on_solution_callback(self):
            solution_dict = {}
            for v in self._variable_list:
                solution_dict[v.Name()] = self.Value(v)
            self._solution_list.append(solution_dict)

        @property
        def solution_tuple(self) -> tuple[dict, ...]:
            return self._solution_list

    _FINGER_INDEX_DOMAIN = cp_model.Domain.FromValues(
        list(music_parameters.constants.HARP_FINGER_INDEX_TO_FINGER.keys())
    )
