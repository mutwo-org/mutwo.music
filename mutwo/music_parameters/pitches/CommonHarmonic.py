from __future__ import annotations

import dataclasses
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


ConcertPitch = core_constants.Real | music_parameters.abc.Pitch


@dataclasses.dataclass(frozen=True)
class Partial(object):
    """Abstract representation of a harmonic spectrum partial.

    :param nth_partial: The number of the partial (starting with 1
        for the root note).
    :type nth_partial: int
    :param tonality: ``True`` for overtone and ``False`` for a (theoretical)
        undertone. Default to ``True``.
    :type tonality: bool

    **Example:**

    >>> from mutwo import music_parameters
    >>> strong_clarinet_partial_tuple = (
    ...     music_parameters.Partial(1, True),
    ...     music_parameters.Partial(3, True),
    ...     music_parameters.Partial(5, True),
    ...     music_parameters.Partial(7, True),
    ... )
    """

    nth_partial: int
    tonality: bool


class CommonHarmonic(JustIntonationPitch):
    """:class:`JustIntonationPitch` which is the common harmonic between two or more other pitches.

    :param partials: Tuple which contains partial numbers.
    :type partials: tuple[Partial, ...]
    :param ratio_or_exponent_tuple: see the documentation of :class:`JustIntonationPitch`
    :type ratio_or_exponent_tuple: str | fractions.Fraction | typing.Iterable[int]
    :param concert_pitch: see the documentation of :class:`JustIntonationPitch`
    :type concert_pitch: core_constants.Real | music_parameters.abc.Pitch
    """

    def __init__(
        self,
        partial_tuple: tuple[Partial, ...],
        ratio_or_exponent_tuple: str
        | fractions.Fraction
        | typing.Iterable[int] = "1/1",
        concert_pitch: ConcertPitch = None,
        *args,
        **kwargs,
    ):
        super().__init__(ratio_or_exponent_tuple, concert_pitch, *args, **kwargs)
        self.partial_tuple = partial_tuple

    def __repr__(self) -> str:
        return f"CommonHarmonic({self.ratio}, {self.partial_tuple})"
