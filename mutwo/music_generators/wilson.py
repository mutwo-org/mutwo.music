"""Algorithms which are related to US-American tuning theorist Erv Wilson."""

import functools
import operator
import itertools
import typing

from mutwo import music_parameters

try:
    from mutwo import common_generators

    BRUN_FOUND = True
except ImportError:
    BRUN_FOUND = False


__all__ = (
    "make_product_pitch",
    "make_common_product_set_scale",
    "make_wilsons_brun_euclidean_algorithm_generator",
)


def make_product_pitch(
    number_sequence: typing.Sequence[int],
    tonality: bool,
    normalize: bool = False,
) -> music_parameters.JustIntonationPitch:
    """Make :class:`~mutwo.core.parameters.music_parameters.JustIntonationPitch` from the product of one, two or more number_sequence.

    :param number_sequence: The number which shall be multiplied to make a new pitch.
    :type number_sequence: typing.Sequence[int]
    :param tonality: ``True`` for putting the resulting product to the numerator of the
        frequency ratio and ``False`` for putting the resulting product to the
        denominator.
    :type tonality: bool
    :param normalize: ``True`` to normalize the new pitch to the middle octave.
        Default to ``False``.
    :type normalize: bool, optional
    """

    product = functools.reduce(operator.mul, number_sequence)
    if tonality:
        ratio = f"{product}/1"
    else:
        ratio = f"1/{product}"

    pitch = music_parameters.JustIntonationPitch(ratio)
    if normalize:
        pitch.normalize()
    return pitch


def make_common_product_set_scale(
    number_sequence: typing.Sequence[int],
    n_combinations: int,
    tonality: bool,
    normalize: bool = False,
) -> tuple[music_parameters.JustIntonationPitch, ...]:
    """Make common product set scale as described in Wilsons letter to Fokker.

    :param number_sequence: The number_sequence which will be combined to single music_parameters.
    :type number_sequence: typing.Sequence[int]
    :param n_combinations: How many number_sequence will be combined for each pitch.
    :type n_combinations: int
    :param tonality: ``True`` for otonality and ``False`` for utonality.
    :type tonality: bool
    :param normalize: ``True`` if music_parameters.shall become normalized to the same octave.
    :type normalize: bool

    **Example:**

    >>> from mutwo import music_generators
    >>> music_generators.make_common_product_set_scale((3, 5, 7, 9), 2, True)
    (JustIntonationPitch('15'), JustIntonationPitch('21'), JustIntonationPitch('27'), JustIntonationPitch('35'), JustIntonationPitch('45'), JustIntonationPitch('63'))
    >>> music_generators.make_common_product_set_scale((3, 5, 7, 9), 2, False)
    (JustIntonationPitch('1/15'), JustIntonationPitch('1/21'), JustIntonationPitch('1/27'), JustIntonationPitch('1/35'), JustIntonationPitch('1/45'), JustIntonationPitch('1/63'))
    """

    common_product_set_scale = []
    for combined_number_sequence in itertools.combinations(
        number_sequence, n_combinations
    ):
        common_product_set_scale.append(
            make_product_pitch(combined_number_sequence, tonality, normalize)
        )

    return tuple(common_product_set_scale)


def make_wilsons_brun_euclidean_algorithm_generator(
    pitch_tuple: tuple[
        music_parameters.JustIntonationPitch,
        music_parameters.JustIntonationPitch,
        music_parameters.JustIntonationPitch,
    ],
    subtraction_index: typing.Literal[1, 2] = 1,
    direction_forward: bool = True,
    direction_reverse: bool = False,
) -> typing.Generator:
    """Make constant structure scale with Wilsons adaption of Bruns euclidean algorithm.

    :param pitch_tuple: The initial seed composed of three individual music_parameters. The
        biggest pitch will be the period of the repeating scale, therefore it is
        recommended to use ``music_parameters.JustIntonationPitch("2/1")`` here (if one
        desires an octave repeating scale).
    :type pitch_tuple: tuple[music_parameters.JustIntonationPitch, music_parameters.JustIntonationPitch, music_parameters.JustIntonationPitch],
    :param subtraction_index: Set to 1 if the largest interval should be subtracted by
        the second interval. Set to 2 if the largest interval should be subtracted by
        the smallest interval.
    :type subtraction_index: int
    :param direction_forward: Set to ``True`` if the algorithm should include the
        normal sorted replacement of an interval. Default to ``True``.
    :type direction_forward: bool
    :param direction_reverse: Set to ``True`` if the algorithm should include the
        reversed replacement of an interval. Default to ``False``.
    :type direction_reverse: bool
    :return: Generator which returns a list of intervals. Accumulate the intervals from
        ``music_parameters.JustIntonationPitch("1/1")`` to get the scale music_parameters.

    **Example:**

    >>> from mutwo import music_parameters
    >>> from mutwo import music_generators
    >>> wilsons_brun_euclidean_algorithm_generator = (
    ...     music_generators.make_wilsons_brun_euclidean_algorithm_generator(
    ...         (
    ...             music_parameters.JustIntonationPitch("2/1"),
    ...             music_parameters.JustIntonationPitch("3/2"),
    ...             music_parameters.JustIntonationPitch("5/4"),
    ...         )
    ...     )
    ... )
    >>> next(wilsons_brun_euclidean_algorithm_generator)
    ((JustIntonationPitch('2/1'),),)
    >>> next(wilsons_brun_euclidean_algorithm_generator)
    ((JustIntonationPitch('3/2'), JustIntonationPitch('4/3')),)
    >>> next(wilsons_brun_euclidean_algorithm_generator)
    ((JustIntonationPitch('4/3'), JustIntonationPitch('9/8'), JustIntonationPitch('4/3')),)
    """

    if not BRUN_FOUND:
        raise ImportError(
            "Generators module 'brun' couldn't be found. "
            "This is most likely because you didn't install "
            "mutwo.ext-common-generators yet."
        )

    try:
        assert direction_forward or direction_reverse
    except AssertionError:
        raise ValueError("Can't set both directions to False!")

    def fetch_first_and_second_interval(
        brun_interval_tuple: tuple[
            music_parameters.JustIntonationPitch,
            music_parameters.JustIntonationPitch,
            music_parameters.JustIntonationPitch,
        ]
    ) -> tuple[
        music_parameters.JustIntonationPitch, music_parameters.JustIntonationPitch
    ]:
        return brun_interval_tuple[0], brun_interval_tuple[subtraction_index]

    bruns_euclidean_algorithm_generator = (
        common_generators.make_bruns_euclidean_algorithm_generator(
            pitch_tuple,
            subtraction_index=subtraction_index,
        )
    )
    brun_interval_tuple = next(bruns_euclidean_algorithm_generator)[0]
    previous_interval, previous_second_interval = fetch_first_and_second_interval(
        brun_interval_tuple
    )
    interval_list_list = [[previous_interval]]
    previous_interval_tuple_tuple = tuple([])

    while True:
        new_interval_tuple_tuple = tuple(map(tuple, interval_list_list))
        if new_interval_tuple_tuple != previous_interval_tuple_tuple:
            yield new_interval_tuple_tuple
        previous_interval_tuple_tuple = new_interval_tuple_tuple
        brun_interval_tuple, _, previous_subtraction_result = next(
            bruns_euclidean_algorithm_generator
        )
        interval_replacement_tuple_list = []
        if direction_forward:
            interval_replacement_tuple_list.append(
                (
                    previous_second_interval,
                    previous_subtraction_result,
                )
            )
        if direction_reverse:
            interval_replacement_tuple_list.append(
                (
                    previous_subtraction_result,
                    previous_second_interval,
                )
            )
        new_interval_list_list = []
        for interval_list in interval_list_list:
            for interval_replacement_tuple in interval_replacement_tuple_list:
                new_interval_list = list(interval_list)
                for index, interval in enumerate(new_interval_list):
                    if interval == previous_interval:
                        new_interval_list[
                            index : index + 1
                        ] = interval_replacement_tuple
                new_interval_list_list.append(new_interval_list)

        interval_list_list = new_interval_list_list

        previous_interval, previous_second_interval = fetch_first_and_second_interval(
            brun_interval_tuple
        )
