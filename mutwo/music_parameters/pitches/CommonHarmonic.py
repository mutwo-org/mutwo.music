from __future__ import annotations

import typing

try:
    import quicktions as fractions  # type: ignore
except ImportError:
    import fractions  # type: ignore


from mutwo import core_constants
from mutwo import music_parameters

from .JustIntonationPitch import JustIntonationPitch

__all__ = (
    "Partial",
    "CommonHarmonic",
)


ConcertPitch = typing.Union[core_constants.Real, music_parameters.abc.Pitch]


class Partial(object):
    """Abstract representation of a harmonic spectrum partial.

    :param nth_partial: The number of the partial (starting with 1
        for the root note).
    :type nth_partial: int
    :param tonality: ``True`` for overtone and ``False`` for a (theoretical)
        undertone. Default to ``True``.
    :type tonality: bool

    **Example:**

    >>> from mutwo.music_parameters import pitches
    >>> strong_clarinet_partials = (
        pitches.Partial(1),
        pitches.Partial(3),
        pitches.Partial(5),
        pitches.Partial(7),
    )
    """

    def __init__(self, nth_partial: int, tonality: bool = True):
        self._nth_partial = nth_partial
        self._tonality = tonality

    @property
    def nth_partial(self) -> int:
        return self._nth_partial

    @property
    def tonality(self) -> int:
        return self._tonality

    def __repr__(self) -> str:
        return f"Partial({self.nth_partial}, {self.tonality})"


class CommonHarmonic(JustIntonationPitch):
    """:class:`JustIntonationPitch` which is the common harmonic between two or more other pitches.

    :param partials: Tuple which contains partial numbers.
    :type partials: tuple[Partial, ...]
    :param ratio_or_exponent_tuple: see the documentation of :class:`JustIntonationPitch`
    :type ratio_or_exponent_tuple: typing.Union[str, fractions.Fraction, typing.Iterable[int]]
    :param concert_pitch: see the documentation of :class:`JustIntonationPitch`
    :type concert_pitch: typing.Union[core_constants.Real, music_parameters.abc.Pitch]
    """

    def __init__(
        self,
        partial_tuple: tuple[Partial, ...],
        ratio_or_exponent_tuple: typing.Union[
            str, fractions.Fraction, typing.Iterable[int]
        ] = "1/1",
        concert_pitch: ConcertPitch = None,
        *args,
        **kwargs,
    ):
        super().__init__(ratio_or_exponent_tuple, concert_pitch, *args, **kwargs)
        self.partial_tuple = partial_tuple

    def __repr__(self) -> str:
        return f"CommonHarmonic({self.ratio}, {self.partial_tuple})"
