import itertools
import typing

try:
    import quicktions as fractions  # type: ignore
except ImportError:
    import fractions  # type: ignore

import gradient_free_optimizers

from mutwo import core_converters
from mutwo import music_parameters


__all__ = ("ImproveWesternPitchListSequenceReadability",)


class ImproveWesternPitchListSequenceReadability(core_converters.abc.Converter):
    """Adjust accidentals of pitches for a tonal-like visual representation

    :param simultaneous_pitch_weight: Factor with which the weights of the
        resulting fitness from pitches of the same pitch list will be
        multiplied. Use higher value if a good form of simultaneous pitches
        is more important for you. Default to 1.
    :type simultaneous_pitch_weight: float
    :param sequential_pitch_weight: Factor with which the weights of the
        resulting fitness from pitches of neighbouring pitch lists will be
        multiplied. Use higher value if a good form of sequential pitches
        is more important for you. Default to 0.7.
    :type sequential_pitch_weight: float
    :param iteration_count: How many iterations the heuristic algorithm shall
        run. Use higher number for better (but slower) results. Default to
        10000.
    :type iteration_count: int
    :param optimizer_class: Sets optimizer class used within the converter.
        This can be any optimizer defined in the
        `gradient_free_optimizers <https://github.com/SimonBlanke/Gradient-Free-Optimizers>`_
        package. Default to
        :class:`gradient_free_optimizers.RandomSearchOptimizer`.
    :type: gradient_free_optimizers.optimizers.base_optimizer.BaseOptimizer,
    :param verbosity_list: From 'gradient_free_optimizers' documentation:
        "The verbosity list determines what part of the optimization
        information will be printed in the command line.". The complete list
        would be `["progress_bar", "print_results", "print_times"]`. Default
        to [] (no logging, silent).
    :param seed: The random seed used within the algorithm. Can be
        `None` for not-deterministic output. Default to 100.
    :type seed: typing.Optional[int]

    This converter aims to adjust :class:`music_parameters.WesternPitch`s in
    order to improve the quality of western notation created with these
    pitches. Non-tonal music should be notated in a way to make it look as
    tonal as possible (e.g. it should notate intervals musicians are used to,
    it should avoid augmented or diminished intervals). The converter aims
    to maximize simple intervals (without changing the actual pitch content)
    by heuristic techniques. The converter may not return the best solution,
    but a very good approximation.

    **Disclaimer:**

    This converter doesn't work with microtonal pitches! This is due to the
    fact that :class:`mutwo.music_parameters.WesternPitchInterval` doesn't
    support microtonal pitches yet.
    """

    PitchVariantListTuple = tuple[list[tuple[music_parameters.WesternPitch, ...]], ...]
    PitchNameTupleToIntervalQualityDict = dict[tuple[str], bool]
    SearchSpace = dict[str, int]
    RealSearchSpace = dict[str, tuple[music_parameters.WesternPitch]]

    _space_separator = "_"

    def __init__(
        self,
        simultaneous_pitch_weight: float = 1,
        sequential_pitch_weight: float = 0.7,
        iteration_count: int = 10000,
        optimizer_class: gradient_free_optimizers.optimizers.base_optimizer.BaseOptimizer = gradient_free_optimizers.RandomSearchOptimizer,
        verbosity_list: list[str] = [],
        seed: typing.Optional[int] = 100,
    ):
        self._simultaneous_pitch_weight = simultaneous_pitch_weight
        self._sequential_pitch_weight = sequential_pitch_weight
        self._iteration_count = iteration_count
        self._optimizer_class = optimizer_class
        self._verbosity_list = verbosity_list
        self._seed = seed

    @staticmethod
    def _get_pitch_variant_tuple(
        western_pitch_to_find_variants_for: music_parameters.WesternPitch,
    ) -> tuple[music_parameters.WesternPitch, ...]:
        try:
            assert not western_pitch_to_find_variants_for.is_microtonal
        except AssertionError:
            raise ValueError(
                "Found illegal microtonal pitch "
                f"'{western_pitch_to_find_variants_for}'. "
                "Converter doesn't support microtonal pitches!"
            )
        western_pitch_base = music_parameters.WesternPitch(
            western_pitch_to_find_variants_for.pitch_class,
            western_pitch_to_find_variants_for.octave,
        )
        return (western_pitch_base,) + western_pitch_base.enharmonic_pitch_tuple

    @staticmethod
    def _get_pitch_variant_list_tuple(
        western_pitch_list_sequence_to_convert: typing.Sequence[
            list[music_parameters.WesternPitch]
        ],
    ) -> PitchVariantListTuple:

        pitch_variant_list_list = []

        for western_pitch_list in western_pitch_list_sequence_to_convert:
            pitch_variant_list = []
            for western_pitch in western_pitch_list:
                pitch_variant_list.append(
                    ImproveWesternPitchListSequenceReadability._get_pitch_variant_tuple(
                        western_pitch
                    )
                )

            pitch_variant_list_list.append(pitch_variant_list)

        return tuple(pitch_variant_list_list)

    @staticmethod
    def _get_pitch_name_tuple_to_interval_quality_dict(
        pitch_variant_list_tuple: PitchVariantListTuple,
    ) -> PitchNameTupleToIntervalQualityDict:
        pitch_class_name_set = set([])
        for pitch_variant_list in pitch_variant_list_tuple:
            for pitch_variant in pitch_variant_list:
                for pitch in pitch_variant:
                    pitch_class_name_set.add(pitch.pitch_class_name)

        pitch_name_tuple_to_interval_quality_dict = {}
        for (
            pitch_class_name0,
            pitch_class_name1,
        ) in itertools.combinations_with_replacement(pitch_class_name_set, 2):
            pitch_interval = music_parameters.WesternPitch(
                pitch_class_name0
            ).get_pitch_interval(music_parameters.WesternPitch(pitch_class_name1))
            can_be_simplified = pitch_interval.can_be_simplified
            pitch_name_tuple_to_interval_quality_dict.update(
                {
                    tuple(
                        sorted([pitch_class_name0, pitch_class_name1])
                    ): can_be_simplified
                }
            )
        return pitch_name_tuple_to_interval_quality_dict

    @staticmethod
    def _get_search_space_and_real_search_space(
        pitch_variant_list_tuple: PitchVariantListTuple,
    ) -> tuple[SearchSpace, RealSearchSpace]:
        search_space = {}
        real_search_space = {}
        for pitch_list_index, pitch_variant_list in enumerate(pitch_variant_list_tuple):
            for pitch_variant_index, pitch_variant in enumerate(pitch_variant_list):
                index_name = "{}{}{}".format(
                    pitch_list_index,
                    ImproveWesternPitchListSequenceReadability._space_separator,
                    pitch_variant_index,
                )
                search_space.update({index_name: tuple(range(len(pitch_variant)))})
                real_search_space.update({index_name: pitch_variant})
        return search_space, real_search_space

    def _get_objective_function(
        self,
        pitch_name_tuple_to_interval_quality_dict: PitchNameTupleToIntervalQualityDict,
        real_search_space: RealSearchSpace,
    ) -> typing.Callable[[dict], float]:
        def compare_two_pitches(
            pitch0: music_parameters.WesternPitch, pitch1: music_parameters.WesternPitch
        ) -> int:
            return pitch_name_tuple_to_interval_quality_dict[
                tuple(sorted([pitch0.pitch_class_name, pitch1.pitch_class_name]))
            ]

        def objective_function(solution: dict[str, int]) -> float:
            fitness = 0
            western_pitch_list_tuple = ImproveWesternPitchListSequenceReadability._get_western_pitch_list_tuple(
                solution, real_search_space
            )
            for western_pitch_list in western_pitch_list_tuple:
                for pitch0, pitch1 in itertools.combinations(western_pitch_list, 2):
                    fitness += (
                        compare_two_pitches(pitch0, pitch1)
                        * self._simultaneous_pitch_weight
                    )

            for western_pitch_list0, western_pitch_list1 in zip(
                western_pitch_list_tuple, western_pitch_list_tuple[1:]
            ):
                for pitch0, pitch1 in itertools.product(
                    western_pitch_list0, western_pitch_list1
                ):
                    fitness += (
                        compare_two_pitches(pitch0, pitch1)
                        * self._sequential_pitch_weight
                    )

            # We prefer if there are not so many double-sharps and
            # double-flats, therefore we will punish the algorithm
            # if there is any (we have to do this because from only
            # interval relationship point-of-view there are often
            # equally acceptable solutions with a lot of accidentals).

            for western_pitch_list in western_pitch_list_tuple:
                for western_pitch in western_pitch_list:
                    if western_pitch.accidental_name in (
                        music_parameters.constants.PITCH_CLASS_MODIFICATION_TO_ACCIDENTAL_NAME_DICT[
                            fractions.Fraction(2, 1)
                        ],
                        music_parameters.constants.PITCH_CLASS_MODIFICATION_TO_ACCIDENTAL_NAME_DICT[
                            -fractions.Fraction(2, 1)
                        ],
                    ):
                        # This is an arbitrary heuristic value, could also be
                        # something else than 2.
                        fitness += 2
                        break

            # This is a MAX optimization; therefore we have to return
            # negative value because it is always +1 if interval
            # `can_be_simplified` (= isn't perfect yet).
            return -fitness

        return objective_function

    @staticmethod
    def _get_western_pitch_list_tuple(
        champion_name_to_champion_value_dict: dict[str, int],
        real_search_space: RealSearchSpace,
    ) -> tuple[list[music_parameters.WesternPitch], ...]:
        western_pitch_list_list = []
        for (
            champion_name,
            western_pitch_index,
        ) in champion_name_to_champion_value_dict.items():
            pitch_list_index, _ = (
                int(index)
                for index in champion_name.split(
                    ImproveWesternPitchListSequenceReadability._space_separator
                )
            )
            while pitch_list_index >= len(western_pitch_list_list):
                western_pitch_list_list.append([])
            western_pitch = real_search_space[champion_name][western_pitch_index]
            western_pitch_list_list[pitch_list_index].append(western_pitch)
        return tuple(western_pitch_list_list)

    def convert(
        self,
        western_pitch_list_sequence_to_convert: typing.Sequence[
            list[music_parameters.WesternPitch]
        ],
    ) -> tuple[list[music_parameters.WesternPitch], ...]:
        """Simplify western pitch notation.

        :param western_pitch_list_sequence_to_convert: A sequence filled
            with lists of :class:`mutwo.music_parameters.WesternPitch`.
            The pitches will be simplified.
        :type western_pitch_list_sequence_to_convert: typing.Sequence[list[music_parameters.WesternPitch]]
        :return: A tuple with lists that contain :class:`music_parameters.WesternPitch`.
            The raw pitch content will be the same as the input
            data, but the accidentals and diatonic pitch class names may
            differ.
        """

        pitch_variant_list_tuple = (
            ImproveWesternPitchListSequenceReadability._get_pitch_variant_list_tuple(
                western_pitch_list_sequence_to_convert
            )
        )
        pitch_name_tuple_to_interval_quality_dict = ImproveWesternPitchListSequenceReadability._get_pitch_name_tuple_to_interval_quality_dict(
            pitch_variant_list_tuple
        )

        # We have to use two different search spaces:
        # The first one which only holds indices and the second
        # one which holds the actual pitch objects (resolutions to
        # these indices). This behaviour is necessary, because
        # the optimizer provided by gradient_free_optimizers
        # can't handle anything else but simple numeric
        # values in its search space (because it applies
        # arithmetic operations on it).
        (
            search_space,
            real_search_space,
        ) = ImproveWesternPitchListSequenceReadability._get_search_space_and_real_search_space(
            pitch_variant_list_tuple
        )
        objective_function = self._get_objective_function(
            pitch_name_tuple_to_interval_quality_dict, real_search_space
        )

        optimizer = self._optimizer_class(search_space, random_state=self._seed)
        optimizer.search(
            objective_function,
            n_iter=self._iteration_count,
            verbosity=self._verbosity_list,
        )

        western_pitch_list_tuple = (
            ImproveWesternPitchListSequenceReadability._get_western_pitch_list_tuple(
                optimizer.best_para, real_search_space
            )
        )

        return western_pitch_list_tuple
