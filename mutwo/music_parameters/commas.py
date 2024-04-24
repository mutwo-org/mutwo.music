"""Abstractions of `tuning commas <https://en.wikipedia.org/wiki/Comma_(music)>`_

The tuning commas are helpful for :class:`mutwo.music_parameters.JustIntonationPitch`
which owns a :attr:`commas` attribute. By default :mod:`mutwo` makes use of commas
defined by the
`Helmholtz-Ellis JI Pitch Notation <https://marsbat.space/pdfs/notation.pdf>`_.
"""

import functools
import operator
import typing

try:
    import quicktions as fractions  # type: ignore
except ImportError:
    import fractions  # type: ignore


__all__ = ("Comma", "CommaCompound")


class Comma(object):
    """A `tuning comma <https://en.wikipedia.org/wiki/Comma_(music)>`_."""

    def __init__(self, ratio: fractions.Fraction):
        self._ratio = ratio

    def __repr__(self) -> str:
        return "Comma({})".format(self.ratio)

    @property
    def ratio(self) -> fractions.Fraction:
        return self._ratio


class CommaCompound(typing.Iterable[Comma]):
    """Collection of tuning commas."""

    # basically a frozen dict?

    def __init__(
        self,
        prime_to_exponent_dict: dict[int, int],
        prime_to_comma_dict: typing.Optional[dict[int, Comma]],
    ):
        # TODO(make sure all primes in 'prime_to_exponent_dict' are also in
        # 'prime_to_comma_dict')

        self._prime_to_exponent_dict = prime_to_exponent_dict
        self._prime_to_comma_dict = prime_to_comma_dict

    def __repr__(self) -> str:
        return "{}({})".format(type(self).__name__, self._prime_to_exponent_dict)

    def __len__(self) -> int:
        return sum((abs(exponent) for exponent in self._prime_to_exponent_dict.values()))

    def __iter__(self):
        return (
            self._prime_to_comma_dict[prime].ratio ** exponent
            for prime, exponent in self._prime_to_exponent_dict.items()
        )

    @property
    def prime_to_exponent_dict(self) -> dict[int, int]:
        return dict(self._prime_to_exponent_dict)

    @property
    def ratio(self) -> fractions.Fraction:
        if self.prime_to_exponent_dict:
            return functools.reduce(operator.mul, iter(self))
        else:
            return fractions.Fraction(1, 1)
