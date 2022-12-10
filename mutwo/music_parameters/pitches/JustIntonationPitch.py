from __future__ import annotations

import collections
import copy
import functools
import math
import operator
import typing
import warnings

from sympy import primepi
from sympy import prime
from sympy import primerange
from sympy.ntheory import factorint

try:
    import quicktions as fractions  # type: ignore
except ImportError:
    import fractions  # type: ignore

from mutwo import core_constants
from mutwo import core_utilities
from mutwo import music_parameters


__all__ = ("JustIntonationPitch",)

ConcertPitch = typing.Union[core_constants.Real, music_parameters.abc.Pitch]
PitchClassOrPitchClassName = typing.Union[core_constants.Real, str]


@functools.total_ordering
class JustIntonationPitch(
    music_parameters.abc.Pitch, music_parameters.abc.PitchInterval
):
    """Pitch that is defined by a frequency ratio and a reference pitch.

    :param ratio_or_exponent_tuple: The frequency ratio of the ``JustIntonationPitch``.
        This can either be a string that indicates the frequency ratio (for
        instance: "1/1", "3/2", "9/2", etc.), or a ``fractions.Fraction``
        object that indicates the frequency ratio (for instance:
        ``fractions.Fraction(3, 2)``, ``fractions.Fraction(7, 4)``) or
        an Iterable that is filled with integer that represents the exponent_tuple
        of the respective prime numbers of the decomposed frequency ratio. The prime
        numbers are rising and start with 2. Therefore the tuple ``(2, 0, -1)``
        would return the frequency ratio ``4/5`` because
        ``(2 ** 2) * (3 ** 0) * (5 ** -1) = 4/5``.
    :param concert_pitch: The reference pitch of the tuning system (the pitch for a
        frequency ratio of 1/1). Can either be another ``Pitch`` object or any number
        to indicate a particular frequency in Hertz.

    The resulting frequency is calculated by multiplying the frequency ratio
    with the respective reference pitch.

    **Example:**

    >>> from mutwo import music_parameters
    >>> # 3 different variations of initialising the same pitch
    >>> music_parameters.JustIntonationPitch('3/2')
    JustIntonationPitch('3/2')
    >>> import fractions
    >>> music_parameters.JustIntonationPitch(fractions.Fraction(3, 2))
    JustIntonationPitch('3/2')
    >>> music_parameters.JustIntonationPitch((-1, 1))
    JustIntonationPitch('3/2')
    >>> # using a different concert pitch
    >>> music_parameters.JustIntonationPitch('7/5', concert_pitch=432)
    JustIntonationPitch('7/5')
    """

    def __init__(
        self,
        ratio_or_exponent_tuple: typing.Union[
            str, fractions.Fraction, typing.Iterable[int]
        ] = "1/1",
        concert_pitch: ConcertPitch = None,
        *args,
        **kwargs,
    ):
        super().__init__(*args, **kwargs)

        if concert_pitch is None:
            concert_pitch = music_parameters.configurations.DEFAULT_CONCERT_PITCH

        self.exponent_tuple = self._ratio_or_fractions_argument_to_exponent_tuple(
            ratio_or_exponent_tuple
        )
        self.concert_pitch = concert_pitch  # type: ignore

    # ###################################################################### #
    #                      static private methods                            #
    # ###################################################################### #

    @staticmethod
    def _adjust_exponent_lengths(
        exponent_tuple0: tuple, exponent_tuple1: tuple
    ) -> tuple:
        r"""Adjust two exponent_tuple, e.g. make their length equal.

        The length of the longer JustIntonationPitch is the reference.

        Arguments:
            * exponent_tuple0: first exponent_tuple to adjust
            * exponent_tuple1: second exponent_tuple to adjust
        >>> v0 = (1, 0, -1)
        >>> v1 = (1,)
        >>> v0_adjusted, v1_adjusted = JustIntonationPitch._adjust_exponent_lengths(v0, v1)
        >>> v0_adjusted
        (1, 0, -1)
        >>> v1_adjusted
        (1, 0, 0)
        """

        length0 = len(exponent_tuple0)
        length1 = len(exponent_tuple1)
        if length0 > length1:
            return exponent_tuple0, exponent_tuple1 + (0,) * (length0 - length1)
        else:
            return exponent_tuple0 + (0,) * (length1 - length0), exponent_tuple1

    @staticmethod
    def _adjust_ratio(ratio: fractions.Fraction, border: int) -> fractions.Fraction:
        r"""Multiply or divide a fractions.Fraction - Object with the border,

        until it is equal or bigger than 1 and smaller than border.

        Arguments:
            * ratio: The Ratio, which shall be adjusted
            * border
        >>> ratio0 = fractions.Fraction(1, 3)
        >>> ratio1 = fractions.Fraction(8, 3)
        >>> border = 2
        >>> JustIntonationPitch._adjust_ratio(ratio0, border)
        Fraction(4, 3)
        >>> JustIntonationPitch._adjust_ratio(ratio1, border)
        Fraction(4, 3)

        """

        if border > 1:
            while ratio >= border:
                ratio /= border
            while ratio < 1:
                ratio *= border
        return ratio

    @staticmethod
    def _adjust_exponent_tuple(
        exponent_tuple: tuple, primes: tuple, border: int
    ) -> tuple:
        r"""Adjust a exponent_tuple and its primes depending on the border.

        Arguments:
            * exponent_tuple: The exponent_tuple, which shall be adjusted
            * primes: Its corresponding primes
            * border
        >>> exponent_tuple0 = (1,)
        >>> primes0 = (3,)
        >>> border = 2
        >>> JustIntonationPitch._adjust_exponent_tuple(exponent_tuple0, primes0, border)
        ((-1, 1), (2, 3))

        """  # TODO(DOCSTRING) Make proper description what actually happens

        if exponent_tuple:
            if border > 1:
                multiplied = functools.reduce(
                    operator.mul, (p**e for p, e in zip(primes, exponent_tuple))
                )
                res = math.log(border / multiplied, border)
                if res < 0:
                    res -= 1
                res = int(res)
                primes = (border,) + primes
                exponent_tuple = (res,) + exponent_tuple
            return exponent_tuple, primes
        return (1,), (1,)

    @staticmethod
    def _discard_nulls(iterable: typing.Iterable[int]) -> tuple[int, ...]:
        r"""Discard all zeros after the last not 0 - element of an arbitary iterable.

        Return a tuple.
        Arguments:
            * iterable: the iterable, whose 0 - elements shall
              be discarded

        >>> tuple0 = (1, 0, 2, 3, 0, 0, 0)
        >>> ls = [1, 3, 5, 0, 0, 0, 2, 0]
        >>> JustIntonationPitch._discard_nulls(tuple0)
        (1, 0, 2, 3)
        >>> JustIntonationPitch._discard_nulls(ls)
        (1, 3, 5, 0, 0, 0, 2)
        """

        iterable = tuple(iterable)
        c = 0
        for i in reversed(iterable):
            if i != 0:
                break
            c += 1
        if c != 0:
            return iterable[:-c]
        return iterable

    @staticmethod
    def _exponent_tuple_to_pair(exponent_tuple: tuple, primes: tuple) -> tuple:
        r"""Transform a JustIntonationPitch to a (numerator, denominator) - pair.

        Arguments are:
            * JustIntonationPitch -> The exponent_tuple of prime numbers
            * primes -> the referring prime numbers
        >>> myJustIntonationPitch0 = (1, 0, -1)
        >>> myJustIntonationPitch1 = (0, 2, 0)
        >>> myVal0 = (2, 3, 5)
        >>> myVal1 = (3, 5, 7)
        >>> JustIntonationPitch._exponent_tuple_to_pair(myJustIntonationPitch0, myVal0)
        (2, 5)
        >>> JustIntonationPitch._exponent_tuple_to_pair(myJustIntonationPitch0, myVal1)
        (3, 7)
        >>> JustIntonationPitch._exponent_tuple_to_pair(myJustIntonationPitch1, myVal1)
        (25, 1)
        """

        numerator = 1
        denominator = 1
        for number, exponent in zip(primes, exponent_tuple):
            if exponent > 0:
                numerator *= pow(number, exponent)
            elif exponent < 0:
                denominator *= pow(number, -exponent)
        return numerator, denominator

    @staticmethod
    def _exponent_tuple_to_ratio(
        exponent_tuple: tuple, primes: tuple
    ) -> fractions.Fraction:
        r"""Transform a JustIntonationPitch to a fractions.Fraction - Object

        (if installed to a quicktions.fractions.Fraction - Object,
        otherwise to a fractions.fractions.Fraction - Object).

        Arguments are:
            * JustIntonationPitch -> The exponent_tuple of prime numbers
            * primes -> the referring prime numbers for the underlying
                      ._exponent_tuple - Argument (see JustIntonationPitch._exponent_tuple).
        >>> exponent_tuple = (1, 0, -1)
        >>> prime_tuple = (2, 3, 5)
        >>> JustIntonationPitch._exponent_tuple_to_ratio(exponent_tuple, prime_tuple)
        Fraction(2, 5)
        """

        numerator, denominator = JustIntonationPitch._exponent_tuple_to_pair(
            exponent_tuple, primes
        )
        return JustIntonationPitch._adjust_ratio(
            fractions.Fraction(numerator, denominator), 1
        )

    @staticmethod
    def _exponent_tuple_to_float(exponent_tuple: tuple, primes: tuple) -> float:
        r"""Transform a JustIntonationPitch to a float.

        Arguments are:
            * JustIntonationPitch -> The exponent_tuple of prime numbers
            * primes -> the referring prime numbers for the underlying
                      ._exponent_tuple - Argument (see JustIntonationPitch._exponent_tuple).
            * primes-shift -> how many prime numbers shall be skipped
                            (see JustIntonationPitch.primes_shift)

        >>> myJustIntonationPitch0 = (1, 0, -1)
        >>> myJustIntonationPitch1 = (0, 2, 0)
        >>> myPrimes = (2, 3, 5)
        >>> JustIntonationPitch._exponent_tuple_to_float(myJustIntonationPitch0, myPrimes)
        0.4
        """

        numerator, denominator = JustIntonationPitch._exponent_tuple_to_pair(
            exponent_tuple, primes
        )
        try:
            return numerator / denominator
        except OverflowError:
            return numerator // denominator

    @staticmethod
    def _ratio_to_exponent_tuple(ratio: fractions.Fraction) -> tuple:
        r"""Transform a fractions.Fraction - Object to a vector of exponent_tuple.

        :param ratio: The fractions.Fraction, which shall be transformed

        **Example:**

        >>> try:
        ...     import quicktions as fractions
        ... except ImportError:
        ...     import fractions
        >>> my_ratio = fractions.Fraction(3, 2)
        >>> JustIntonationPitch._ratio_to_exponent_tuple(my_ratio)
        (-1, 1)
        """

        factorised_numerator = factorint(ratio.numerator)
        factorised_denominator = factorint(ratio.denominator)

        try:
            biggest_prime = max(
                tuple(factorised_numerator.keys())
                + tuple(factorised_denominator.keys())
            )
        except ValueError:
            biggest_prime = 2

        exponent_tuple = [0] * primepi(biggest_prime)

        for prime, factor in factorised_numerator.items():
            if prime > 1:
                exponent_tuple[primepi(prime) - 1] += factor

        for prime, factor in factorised_denominator.items():
            if prime > 1:
                exponent_tuple[primepi(prime) - 1] -= factor

        return tuple(exponent_tuple)

    @staticmethod
    def _indigestibility(num: int) -> float:
        """Calculate _indigestibility of a number

        The implementation follows Clarence Barlows definition
        given in 'The Ratio Book' (1992).
        Arguments:
            * num -> integer, whose _indigestibility value shall be calculated

        **Example:**

        >>> JustIntonationPitch._indigestibility(1)
        0
        >>> JustIntonationPitch._indigestibility(2)
        1.0
        >>> JustIntonationPitch._indigestibility(3)
        2.6666666666666665
        """

        decomposed = factorint(num, multiple=True)
        return JustIntonationPitch._indigestibility_of_factorised(decomposed)

    @staticmethod
    def _indigestibility_of_factorised(decomposed):
        decomposed = collections.Counter(decomposed)
        decomposed = zip(decomposed.values(), decomposed.keys())
        summed = ((power * pow(prime - 1, 2)) / prime for power, prime in decomposed)
        return 2 * sum(summed)

    @staticmethod
    def _count_accidentals(accidentals: str) -> int:
        accidental_counter = collections.Counter({"f": 0, "s": 0})
        accidental_counter.update(accidentals)
        for accidental in accidentals:
            if accidental not in ("f", "s"):
                warnings.warn(
                    f"Found unknown accidental '{accidental}' which will be ignored",
                    RuntimeWarning,
                )
        return (1 * accidental_counter["s"]) - (1 * accidental_counter["f"])

    @staticmethod
    def _get_accidentals(n_accidentals: int) -> str:
        if n_accidentals > 0:
            return "s" * n_accidentals
        else:
            return "f" * abs(n_accidentals)

    # ###################################################################### #
    #                            private methods                             #
    # ###################################################################### #

    def _ratio_or_fractions_argument_to_exponent_tuple(
        self,
        ratio_or_exponent_tuple: typing.Union[
            str, fractions.Fraction, typing.Iterable[int]
        ],
    ) -> tuple[int, ...]:
        if isinstance(ratio_or_exponent_tuple, str):
            numerator, denominator = ratio_or_exponent_tuple.split("/")
            exponent_tuple = self._ratio_to_exponent_tuple(
                fractions.Fraction(int(numerator), int(denominator))
            )
        elif isinstance(ratio_or_exponent_tuple, typing.Iterable):
            exponent_tuple = tuple(ratio_or_exponent_tuple)
        elif hasattr(ratio_or_exponent_tuple, "numerator") and hasattr(
            ratio_or_exponent_tuple, "denominator"
        ):
            exponent_tuple = self._ratio_to_exponent_tuple(
                fractions.Fraction(
                    ratio_or_exponent_tuple.numerator,
                    ratio_or_exponent_tuple.denominator,
                )
            )
        else:
            raise NotImplementedError(
                f"Unknown type '{type(ratio_or_exponent_tuple)}' of object "
                f"'{ratio_or_exponent_tuple}' for 'ratio_or_exponent_tuple' "
                "argument."
            )
        return exponent_tuple

    @core_utilities.add_copy_option
    def _math(  # type: ignore
        self, other: JustIntonationPitch, operation: typing.Callable
    ) -> JustIntonationPitch:
        exponent_tuple0, exponent_tuple1 = JustIntonationPitch._adjust_exponent_lengths(
            self.exponent_tuple, other.exponent_tuple
        )
        self.exponent_tuple = tuple(
            operation(exponent0, exponent1)
            for exponent0, exponent1 in zip(exponent_tuple0, exponent_tuple1)
        )

    # ###################################################################### #
    #                            magic methods                               #
    # ###################################################################### #

    def __eq__(self, other: typing.Any) -> bool:
        match other:
            case JustIntonationPitch():
                return self.exponent_tuple == other.exponent_tuple
            case music_parameters.abc.PitchInterval():
                return self.interval == other.interval
            case _:  # pitch test
                return super().__eq__(other)

    def __lt__(self, other: typing.Any) -> bool:
        match other:
            case music_parameters.abc.PitchInterval():
                return self.interval < other.interval
            case _:  # pitch test
                return super().__lt__(self, other)

    def __float__(self) -> float:
        """Return the float of a JustIntonationPitch - object.

        These are the same:
            float(myJustIntonationPitch.ratio) == float(myJustIntonationPitch).
        Note the difference that the second version might be slightly
        more performant.

        **Example:**

        >>> just_intonation_pitch0 = JustIntonationPitch((-1, 1))
        >>> float(just_intonation_pitch0)
        1.5
        >>> float(just_intonation_pitch0.ratio)
        1.5
        """

        return self._exponent_tuple_to_float(self.exponent_tuple, self.prime_tuple)

    def __repr__(self) -> str:
        ratio = str(self.ratio)
        if len(ratio) == 1:
            ratio += "/1"
        return f"{type(self).__name__}('{ratio}')"

    def __abs__(self):
        if self.numerator > self.denominator:
            return copy.deepcopy(self)
        else:
            exponent_tuple = tuple(-v for v in iter(self.exponent_tuple))
            return type(self)(exponent_tuple, self.concert_pitch)

    # ###################################################################### #
    #                            properties                                  #
    # ###################################################################### #

    @property
    def exponent_tuple(self) -> tuple:
        return self._exponent_tuple

    @exponent_tuple.setter
    def exponent_tuple(
        self,
        exponent_tuple: typing.Iterable[int],
    ) -> None:
        self._exponent_tuple = self._discard_nulls(exponent_tuple)

    @property
    def prime_tuple(self) -> tuple:
        r"""Return ascending list of primes, until the highest contained Prime.

        **Example:**

        >>> just_intonation_pitch0 = JustIntonationPitch((0, 1, 2))
        >>> just_intonation_pitch0.prime_tuple
        (2, 3, 5)
        >>> just_intonation_pitch1 = JustIntonationPitch((0, -1, 0, 0, 1), 1)
        >>> just_intonation_pitch1.prime_tuple
        (2, 3, 5, 7, 11)
        """

        return tuple(primerange(prime(len(self.exponent_tuple) + 1)))

    @property
    def occupied_primes(self) -> tuple:
        """Return all occurring prime numbers of a JustIntonationPitch object."""

        return tuple(
            prime
            for prime, exponent in zip(self.prime_tuple, self.exponent_tuple)
            if exponent != 0
        )

    @property
    def concert_pitch(self) -> music_parameters.abc.Pitch:
        return self._concert_pitch

    @concert_pitch.setter
    def concert_pitch(self, concert_pitch: ConcertPitch) -> None:
        if not isinstance(concert_pitch, music_parameters.abc.Pitch):
            concert_pitch = music_parameters.DirectPitch(concert_pitch)

        self._concert_pitch = concert_pitch

    @property
    def frequency(self) -> float:
        return float(self.ratio * self.concert_pitch.frequency)

    @property
    def ratio(self) -> fractions.Fraction:
        """Return the JustIntonationPitch transformed to a Ratio.

        **Example:**

        >>> just_intonation_pitch = JustIntonationPitch((0, 0, 1,))
        >>> just_intonation_pitch.ratio
        Fraction(5, 1)
        >>> just_intonation_pitch = JustIntonationPitch("3/2")
        >>> just_intonation_pitch.ratio
        Fraction(3, 2)
        """

        return JustIntonationPitch._exponent_tuple_to_ratio(
            self.exponent_tuple, self.prime_tuple
        )

    @property
    def numerator(self) -> int:
        """Return the numerator of a JustIntonationPitch - object.

        **Example:**

        >>> just_intonation_pitch0 = JustIntonationPitch((0, -1,))
        >>> just_intonation_pitch0.numerator
        1
        """

        numerator = 1
        for number, exponent in zip(self.prime_tuple, self.exponent_tuple):
            if exponent > 0:
                numerator *= pow(number, exponent)
        return numerator

    @property
    def denominator(self) -> int:
        """Return the denominator of :class:`JustIntonationPitch`.

        **Example:**

        >>> just_intonation_pitch0 = JustIntonationPitch((0, 1,))
        >>> just_intonation_pitch0.denominator
        1
        """

        denominator = 1
        for number, exponent in zip(self.prime_tuple, self.exponent_tuple):
            if exponent < 0:
                denominator *= pow(number, -exponent)
        return denominator

    @property
    def interval(self) -> float:
        return self.ratio_to_cents(self.ratio)

    @property
    def factorised(self) -> tuple:
        """Return factorised / decomposed version of itsef.

        **Example:**

        >>> just_intonation_pitch0 = JustIntonationPitch((-2, 0, 1))
        >>> just_intonation_pitch0.factorised
        (2, 2, 5)
        >>> just_intonation_pitch1 = JustIntonationPitch("7/6")
        >>> just_intonation_pitch1.factorised
        (2, 3, 7)
        """

        exponent_tuple = self.exponent_tuple
        prime_tuple = self.prime_tuple
        exponent_tuple_adjusted, prime_tuple_adjusted = type(
            self
        )._adjust_exponent_tuple(exponent_tuple, prime_tuple, 1)
        decomposed = (
            [prime] * abs(exponent)
            for prime, exponent in zip(prime_tuple_adjusted, exponent_tuple_adjusted)
        )
        return tuple(functools.reduce(operator.add, decomposed))

    @property
    def factorised_numerator_and_denominator(self) -> tuple:
        exponent_tuple = self.exponent_tuple
        prime_tuple = self.prime_tuple
        exponent_tuple_adjusted, prime_tuple_adjusted = type(
            self
        )._adjust_exponent_tuple(exponent_tuple, prime_tuple, 1)
        numerator_denominator: list[list[list[int]]] = [[[]], [[]]]
        for prime, exponent in zip(prime_tuple_adjusted, exponent_tuple_adjusted):
            if exponent > 0:
                index = 0
            else:
                index = 1
            numerator_denominator[index].append([prime] * abs(exponent))
        return tuple(
            functools.reduce(operator.add, decomposed)
            for decomposed in numerator_denominator
        )

    @property
    def octave(self) -> int:
        return int(self.interval // music_parameters.constants.OCTAVE_IN_CENTS)

    @property
    def helmholtz_ellis_just_intonation_notation_commas(
        self,
    ) -> music_parameters.CommaCompound:
        """Commas of JustIntonationPitch."""

        prime_to_exponent_dict = {
            prime: exponent
            for prime, exponent in zip(self.prime_tuple, self.exponent_tuple)
            if exponent != 0 and prime not in (2, 3)
        }
        return music_parameters.CommaCompound(
            prime_to_exponent_dict,
            music_parameters.configurations.DEFAULT_PRIME_TO_COMMA_DICT,
        )

    @property
    def closest_pythagorean_interval(self) -> JustIntonationPitch:
        if len(self.helmholtz_ellis_just_intonation_notation_commas) > 0:
            closest_pythagorean_interval = self - type(self)(
                functools.reduce(
                    operator.mul, self.helmholtz_ellis_just_intonation_notation_commas
                )
            )
            closest_pythagorean_interval.normalize()
        else:
            closest_pythagorean_interval = self.normalize(mutate=False)  # type: ignore

        return closest_pythagorean_interval

    @property
    def cent_deviation_from_closest_western_pitch_class(self) -> float:
        deviation_by_helmholtz_ellis_just_intonation_notation_commas = (
            JustIntonationPitch(
                self.helmholtz_ellis_just_intonation_notation_commas.ratio
            ).interval
        )
        closest_pythagorean_interval = self.closest_pythagorean_interval
        if len(closest_pythagorean_interval.exponent_tuple) >= 2:
            pythagorean_deviation = self.closest_pythagorean_interval.exponent_tuple[
                1
            ] * (JustIntonationPitch("3/2").interval - 700)
        else:
            pythagorean_deviation = 0
        return (
            deviation_by_helmholtz_ellis_just_intonation_notation_commas
            + pythagorean_deviation
        )

    @property
    def blueprint(  # type: ignore
        self, ignore: typing.Sequence[int] = (2,)
    ) -> tuple[tuple[int, ...], ...]:
        blueprint = []
        for factorised in self.factorised_numerator_and_denominator:
            factorised = tuple(fac for fac in factorised if fac not in ignore)
            counter = collections.Counter(collections.Counter(factorised).values())
            if counter:
                maxima = max(counter.keys())
                blueprint.append(tuple(counter[index + 1] for index in range(maxima)))
            else:
                blueprint.append(tuple([]))
        return tuple(blueprint)

    @property
    def tonality(self) -> bool:
        """Return the tonality (bool) of a JustIntonationPitch - object.

        The tonality of a JustIntonationPitch   - may be True (otonality) if
        the exponent of the highest occurring prime number is a
        positive number and False if the exponent is a
        negative number (utonality).

        **Example:**

        >>> from mutwo import music_parameters
        >>> just_intonation_pitch0 = music_parameters.JustIntonationPitch((-2, 1))
        >>> just_intonation_pitch0.tonality
        True
        >>> just_intonation_pitch1 = music_parameters.JustIntonationPitch((-2, -1))
        >>> just_intonation_pitch1.tonality
        False
        >>> just_intonation_pitch2 = music_parameters.JustIntonationPitch([])
        >>> just_intonation_pitch2.tonality
        True
        """

        if self.exponent_tuple:
            maxima = max(self.exponent_tuple)
            minima = min(self.exponent_tuple)
            test = (
                maxima <= 0 and minima < 0,
                minima < 0
                and self.exponent_tuple.index(minima)
                > self.exponent_tuple.index(maxima),
            )
            if any(test):
                return False

        return True

    @property
    def harmonic(self) -> int:
        """Return the nth - harmonic / subharmonic the pitch may represent.

        :return: May be positive for harmonic and negative for
            subharmonic pitches. If the return - value is 0,
            the interval may occur neither between the first harmonic
            and any other pitch of the harmonic scale nor
            between the first subharmonic in the and any other
            pitch of the subharmonic scale.

        **Example:**

        >>> just_intonation_pitch0 = JustIntonationPitch((-1, 1))
        >>> just_intonation_pitch0.ratio
        Fraction(3, 2)
        >>> just_intonation_pitch0.harmonic
        3
        >>> just_intonation_pitch1 = JustIntonationPitch((1, -1))
        >>> just_intonation_pitch1.harmonic
        -3
        """

        ratio = self.ratio

        if ratio.denominator % 2 == 0:
            return ratio.numerator
        elif ratio.numerator % 2 == 0:
            return -ratio.denominator
        elif ratio == fractions.Fraction(1, 1):
            return 1
        else:
            return 0

    @property
    def primes_for_numerator_and_denominator(self) -> tuple:
        return tuple(
            tuple(sorted(set(factorint(n, multiple=True))))
            for n in (self.numerator, self.denominator)
        )

    @property
    def harmonicity_wilson(self) -> int:
        decomposed = self.factorised
        return int(sum(filter(lambda x: x != 2, decomposed)))

    @property
    def harmonicity_vogel(self) -> int:
        decomposed = self.factorised
        decomposed_filtered = tuple(filter(lambda x: x != 2, decomposed))
        am_2 = len(decomposed) - len(decomposed_filtered)
        return int(sum(decomposed_filtered) + am_2)

    @property
    def harmonicity_euler(self) -> int:
        """Return the 'gradus suavitatis' of euler.

        A higher number means a less consonant interval /
        a more complicated harmony.
        euler(1/1) is definied as 1.

        **Example:**

        >>> just_intonation_pitch0 = JustIntonationPitch((-1, 1))
        >>> just_intonation_pitch1 = JustIntonationPitch()
        >>> just_intonation_pitch2 = JustIntonationPitch((-2, 0, 1))
        >>> just_intonation_pitch3 = JustIntonationPitch((-3, 0, -1))
        >>> just_intonation_pitch0.harmonicity_euler
        4
        >>> just_intonation_pitch1.harmonicity_euler
        1
        >>> just_intonation_pitch2.harmonicity_euler
        7
        >>> just_intonation_pitch3.harmonicity_euler
        8
        """

        decomposed = self.factorised
        return 1 + sum(x - 1 for x in decomposed)

    @property
    def harmonicity_barlow(self) -> float:
        r"""Calculate the barlow-harmonicity of an interval.

        This implementation follows Clarence Barlows definition, given
        in 'The Ratio Book' (1992).

        A higher number means a more harmonic interval / a less
        complex harmony.

        barlow(1/1) is definied as infinite.

        **Example:**

        >>> just_intonation_pitch0 = JustIntonationPitch((-1, 1))
        >>> just_intonation_pitch1 = JustIntonationPitch()
        >>> just_intonation_pitch2 = JustIntonationPitch((-2, 0, 1))
        >>> just_intonation_pitch3 = JustIntonationPitch((-3, 0, -1))
        >>> just_intonation_pitch0.harmonicity_barlow
        0.27272727272727276
        >>> just_intonation_pitch1.harmonicity_barlow # 1/1 is infinite harmonic
        inf
        >>> just_intonation_pitch2.harmonicity_barlow
        0.11904761904761904
        >>> just_intonation_pitch3.harmonicity_barlow
        -0.10638297872340426
        """

        def sign(x):
            return (1, -1)[x < 0]

        numerator_denominator_decomposed = self.factorised_numerator_and_denominator
        indigestibility_numerator = JustIntonationPitch._indigestibility_of_factorised(
            numerator_denominator_decomposed[0]
        )
        indigestibility_denominator = (
            JustIntonationPitch._indigestibility_of_factorised(
                numerator_denominator_decomposed[1]
            )
        )
        if indigestibility_numerator == 0 and indigestibility_denominator == 0:
            return float("inf")
        return sign(indigestibility_numerator - indigestibility_denominator) / (
            indigestibility_numerator + indigestibility_denominator
        )

    @property
    def harmonicity_simplified_barlow(self) -> float:
        r"""Calculate a simplified barlow-harmonicity of an interval.

        This implementation follows Clarence Barlows definition, given
        in 'The Ratio Book' (1992), with the difference that
        only positive numbers are returned and that (1/1) is
        defined as 1 instead of infinite.

        >>> just_intonation_pitch0 = JustIntonationPitch((-1, 1))
        >>> just_intonation_pitch1 = JustIntonationPitch()
        >>> just_intonation_pitch2 = JustIntonationPitch((-2, 0, 1))
        >>> just_intonation_pitch3 = JustIntonationPitch((-3, 0, -1))
        >>> just_intonation_pitch0.harmonicity_simplified_barlow
        0.27272727272727276
        >>> just_intonation_pitch1.harmonicity_simplified_barlow # 1/1 is not infinite but 1
        1
        >>> just_intonation_pitch2.harmonicity_simplified_barlow
        0.11904761904761904
        >>> just_intonation_pitch3.harmonicity_simplified_barlow # positive return value
        0.10638297872340426
        """

        barlow = abs(self.harmonicity_barlow)
        if barlow == float("inf"):
            return 1
        return barlow

    @property
    def harmonicity_tenney(self) -> float:
        r"""Calculate Tenneys harmonic distance of an interval

        A higher number
        means a more consonant interval / a less
        complicated harmony.

        tenney(1/1) is definied as 0.

        >>> just_intonation_pitch0 = JustIntonationPitch((0, 1,))
        >>> just_intonation_pitch1 = JustIntonationPitch()
        >>> just_intonation_pitch2 = JustIntonationPitch((0, 0, 1,))
        >>> just_intonation_pitch3 = JustIntonationPitch((0, 0, -1,))
        >>> just_intonation_pitch0.harmonicity_tenney
        1.5849625007211563
        >>> just_intonation_pitch1.harmonicity_tenney
        0.0
        >>> just_intonation_pitch2.harmonicity_tenney
        2.321928094887362
        >>> just_intonation_pitch3.harmonicity_tenney
        2.321928094887362
        """

        ratio = self.ratio
        return math.log(ratio.numerator * ratio.denominator, 2)

    # ###################################################################### #
    #                            public methods                              #
    # ###################################################################### #

    def get_closest_pythagorean_pitch_name(self, reference: str = "a") -> str:
        """"""

        # TODO(for future usage: type reference as typing.Literal[] instead of str)

        # TODO(split method, make it more readable)

        # TODO(Add documentation)

        diatonic_pitch_name, accidentals = reference[0], reference[1:]
        n_accidentals_in_reference = JustIntonationPitch._count_accidentals(accidentals)
        position_of_diatonic_pitch_in_cycle_of_fifths = (
            music_parameters.constants.DIATONIC_PITCH_NAME_CYCLE_OF_FIFTH_TUPLE.index(
                diatonic_pitch_name
            )
        )

        closest_pythagorean_interval = self.closest_pythagorean_interval
        try:
            n_fifths = closest_pythagorean_interval.exponent_tuple[1]
        # for 1/1
        except IndexError:
            n_fifths = 0

        # 1. Find new diatonic pitch name
        n_steps_in_diatonic_pitch_name = n_fifths % 7
        nth_diatonic_pitch = (
            position_of_diatonic_pitch_in_cycle_of_fifths
            + n_steps_in_diatonic_pitch_name
        ) % 7
        new_diatonic_pitch = (
            music_parameters.constants.DIATONIC_PITCH_NAME_CYCLE_OF_FIFTH_TUPLE[
                nth_diatonic_pitch
            ]
        )

        # 2. Find new accidentals
        n_accidentals_in_closest_pythagorean_pitch = (
            (position_of_diatonic_pitch_in_cycle_of_fifths + n_fifths) // 7
        ) + n_accidentals_in_reference
        new_accidentals = JustIntonationPitch._get_accidentals(
            n_accidentals_in_closest_pythagorean_pitch
        )

        return "".join((new_diatonic_pitch, new_accidentals))

    def get_pitch_interval(
        self, pitch_to_compare: music_parameters.abc.Pitch
    ) -> music_parameters.abc.PitchInterval:
        if isinstance(pitch_to_compare, JustIntonationPitch):
            return pitch_to_compare - self
        else:
            return super().get_pitch_interval(pitch_to_compare)

    @core_utilities.add_copy_option
    def register(self, octave: int) -> JustIntonationPitch:  # type: ignore
        """Move :class:`JustIntonationPitch` to the given octave.

        :param octave: 0 for the octave from 1/1 to 2/1, negative values for octaves
            below 1/1 and positive values for octaves above 2/1.
        :type octave: int

        **Example:**

        >>> from mutwo.music_parameters import pitches
        >>> p = pitches.JustIntonationPitch('3/2')
        >>> p.register(1)
        JustIntonationPitch('3/1')
        >>> p
        JustIntonationPitch('3/1')
        >>> p.register(-1)
        JustIntonationPitch('3/4')
        >>> p
        JustIntonationPitch('3/4')
        >>> p.register(0)
        JustIntonationPitch('3/2')
        >>> p
        JustIntonationPitch('3/2')
        """

        normalized_just_intonation_pitch = self.normalize(mutate=False)  # type: ignore
        factor = 2 ** abs(octave)
        if octave < 1:
            added = type(self)(fractions.Fraction(1, factor))
        else:
            added = type(self)(fractions.Fraction(factor, 1))
        self.exponent_tuple = (normalized_just_intonation_pitch + added).exponent_tuple  # type: ignore

    @core_utilities.add_copy_option
    def move_to_closest_register(  # type: ignore
        self, reference: JustIntonationPitch
    ) -> JustIntonationPitch:
        reference_register = reference.octave

        best = None
        for adaption in range(-1, 2):
            candidate: JustIntonationPitch = self.register(reference_register + adaption, mutate=False)  # type: ignore
            difference = abs((candidate - reference).interval)
            set_best = True
            if best and difference > best[1]:
                set_best = False

            if set_best:
                best = (candidate, difference)

        if best:
            self.exponent_tuple = best[0].exponent_tuple
        else:
            raise NotImplementedError(
                f"Couldn't find closest register of '{self}' to '{reference}'."
            )

    @core_utilities.add_copy_option
    def normalize(self, prime: int = 2) -> JustIntonationPitch:  # type: ignore
        """Normalize :class:`JustIntonationPitch`.

        :param prime: The normalization period (2 for octave,
            3 for twelfth, ...). Default to 2.
        :type prime: int

        **Example:**

        >>> from mutwo.music_parameters import pitches
        >>> p = pitches.JustIntonationPitch('12/2')
        >>> p.normalize()
        JustIntonationPitch('3/2')
        >>> p
        JustIntonationPitch('3/2')
        """
        ratio = self.ratio
        adjusted = type(self)._adjust_ratio(ratio, prime)
        self.exponent_tuple = self._ratio_or_fractions_argument_to_exponent_tuple(
            adjusted
        )

    @core_utilities.add_copy_option
    def inverse(  # type: ignore
        self, axis: typing.Optional[JustIntonationPitch] = None
    ) -> JustIntonationPitch:
        """Inverse current pitch on given axis.

        :param axis: The :class:`JustIntonationPitch` from which the
            pitch shall be inversed.
        :type axis: JustIntonationPitch, optional

        **Example:**

        >>> from mutwo.music_parameters import pitches
        >>> p = pitches.JustIntonationPitch('3/2')
        >>> p.inverse()
        JustIntonationPitch('2/3')
        >>> p
        JustIntonationPitch('2/3')
        """

        if axis is None:
            exponent_tuple = tuple(map(lambda x: -x, self.exponent_tuple))
        else:
            distance = self - axis
            exponent_tuple = (axis - distance).exponent_tuple
        self.exponent_tuple = exponent_tuple

    @core_utilities.add_copy_option
    def add(
        self, pitch_interval: music_parameters.abc.PitchInterval
    ) -> JustIntonationPitch:
        """Add :class:`JustIntonationPitch` to current pitch.

        :param other: The :class:`JustIntonationPitch` to add to
            the current pitch.

        **Example:**

        >>> from mutwo.music_parameters import pitches
        >>> p = pitches.JustIntonationPitch('3/2')
        >>> p.add(pitches.JustIntonationPitch('3/2'))
        JustIntonationPitch('9/4')
        >>> p
        JustIntonationPitch('9/4')
        """
        if isinstance(pitch_interval, JustIntonationPitch):
            self._math(pitch_interval, operator.add)
        else:
            self.exponent_tuple = self._ratio_to_exponent_tuple(
                self.ratio * self.cents_to_ratio(pitch_interval.interval)
            )
        return self

    @core_utilities.add_copy_option
    def subtract(
        self, pitch_interval: music_parameters.abc.PitchInterval
    ) -> JustIntonationPitch:
        """Subtract :class:`JustIntonationPitch` from current pitch.

        :param other: The :class:`JustIntonationPitch` to subtract from
            the current pitch.

        **Example:**

        >>> from mutwo import music_parameters
        >>> p = music_parameters.JustIntonationPitch('9/4')
        >>> p.subtract(music_parameters.JustIntonationPitch('3/2'))
        JustIntonationPitch('3/2')
        >>> p
        JustIntonationPitch('3/2')
        """

        if isinstance(pitch_interval, JustIntonationPitch):
            self._math(pitch_interval, operator.sub)
        else:
            self.exponent_tuple = self._ratio_to_exponent_tuple(
                self.ratio / self.cents_to_ratio(pitch_interval.interval)
            )
        return self

    @core_utilities.add_copy_option
    def intersection(
        self, other: JustIntonationPitch, strict: bool = False
    ) -> JustIntonationPitch:
        """Make intersection with other :class:`JustIntonationPitch`.

        :param other: The :class:`JustIntonationPitch` to build the
            intersection with.
        :param strict: If set to ``True`` only exponent_tuple are included
            into the intersection if their value is equal. If set to
            ``False`` the method will also include exponent_tuple if both
            pitches own them on the same axis but with different values
            (the method will take the smaller exponent).
        :type strict: bool

        **Example:**

        >>> from mutwo import music_parameters
        >>> p0 = music_parameters.JustIntonationPitch('5/3')
        >>> p0.intersection(music_parameters.JustIntonationPitch('7/6'))
        JustIntonationPitch('1/3')
        >>> p0
        JustIntonationPitch('1/3')
        >>> p1 = music_parameters.JustIntonationPitch('9/7')
        >>> p1.intersection(music_parameters.JustIntonationPitch('3/2'))
        JustIntonationPitch('3/1')
        >>> p1
        JustIntonationPitch('3/1')
        >>> p2 = music_parameters.JustIntonationPitch('9/7')
        >>> p2.intersection(music_parameters.JustIntonationPitch('3/2'), strict=True)
        JustIntonationPitch('1/1')
        >>> p2
        JustIntonationPitch('1/1')
        """

        def is_negative(number: int):
            return number < 0

        def intersect_exponent_tuple(exponent_tuple: tuple[int, int]) -> int:
            intersected_exponent = 0

            if strict:
                test_for_valid_strict_mode = exponent_tuple[0] == exponent_tuple[1]
            else:
                test_for_valid_strict_mode = True

            if 0 not in exponent_tuple and test_for_valid_strict_mode:
                are_negative = (is_negative(exponent) for exponent in exponent_tuple)
                all_are_negative = all(are_negative)
                all_are_positive = all(not boolean for boolean in are_negative)

                if all_are_negative:
                    intersected_exponent = max(exponent_tuple)
                elif all_are_positive:
                    intersected_exponent = min(exponent_tuple)

            return intersected_exponent

        intersected_exponent_tuple = tuple(
            map(
                intersect_exponent_tuple, zip(self.exponent_tuple, other.exponent_tuple)
            )
        )
        self.exponent_tuple = intersected_exponent_tuple
