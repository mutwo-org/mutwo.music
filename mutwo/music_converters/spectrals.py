import typing

from mutwo import core_converters
from mutwo import music_parameters

__all__ = ("TwoPitchesToCommonHarmonicTuple",)


class TwoPitchesToCommonHarmonicTuple(core_converters.abc.Converter):
    """Find the common harmonics between two pitches.

    :param tonality: ``True`` for finding common harmonics, ``False`` for finding
        common subharmonics and ``None`` for finding common pitches between the
        harmonics of the first pitch and the subharmonics of the second pitch.
    :type tonality: typing.Optional[bool]
    :param lowest_partial: The lowest partial to get investigated. Shouldn't be smaller
        than 1.
    :type lowest_partial: int
    :param highest_partial: The highest partial to get investigated. Shouldn't be bigger
        than 1.
    :type highest_partial: int
    """

    def __init__(
        self, tonality: typing.Optional[bool], lowest_partial: int, highest_partial: int
    ):
        self._tonality_per_pitch_tuple = (
            (tonality, tonality) if tonality is not None else (True, False)
        )
        self._tonality_to_partial_tuple_dict = {
            tonality: TwoPitchesToCommonHarmonicTuple._make_partials(
                lowest_partial, highest_partial, tonality
            )
            for tonality in (True, False)
        }

    @staticmethod
    def _make_partials(
        lowest_partial: int, highest_partial: int, tonality: bool
    ) -> tuple[tuple[int, music_parameters.JustIntonationPitch], ...]:
        partial_tuple = tuple(
            (partial_index, music_parameters.JustIntonationPitch(partial_index, 1))
            for partial_index in range(lowest_partial, highest_partial)
        )
        if not tonality:
            [partial.inverse() for _, partial in partial_tuple]
        return partial_tuple

    def convert(
        self,
        pitch_pair_to_examine: tuple[
            music_parameters.JustIntonationPitch,
            music_parameters.JustIntonationPitch,
        ],
    ) -> tuple[music_parameters.CommonHarmonic, ...]:
        partials0, partials1 = tuple(
            tuple(
                (partial_index, partial + pitch)
                for partial_index, partial in self._tonality_to_partial_tuple_dict[
                    tonality
                ]
            )
            for pitch, tonality in zip(
                pitch_pair_to_examine, self._tonality_per_pitch_tuple
            )
        )

        partial_index_for_partials1, partials1 = zip(*partials1)

        common_harmonic_list = []
        for partial_index_for_first_pitch, partial in partials0:
            if partial in partials1:
                partial_index_for_second_pitch = partial_index_for_partials1[
                    partials1.index(partial)
                ]
                common_harmonic = music_parameters.CommonHarmonic(
                    tuple(
                        music_parameters.Partial(partial_index, tonality)
                        for partial_index, tonality in zip(
                            (
                                partial_index_for_first_pitch,
                                partial_index_for_second_pitch,
                            ),
                            self._tonality_per_pitch_tuple,
                        )
                    ),
                    partial,
                )
                common_harmonic_list.append(common_harmonic)

        return tuple(common_harmonic_list)
