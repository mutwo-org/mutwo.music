"""Abstract base classes for different parameters.

This module defines the public API of parameters.
Most other mutwo classes rely on this API. This means
when someone creates a new class inheriting from any of the
abstract parameter classes which are defined in this module,
she or he can make use of all other mutwo modules with this
newly created parameter class.
"""

from __future__ import annotations

import abc
import ast
import copy
import dataclasses
import functools
import math
import numbers
import types
import typing

try:
    import quicktions as fractions  # type: ignore
except ImportError:
    import fractions  # type: ignore

    _fractions = None
else:
    import fractions as _fractions

import ranges

from mutwo import core_constants
from mutwo import core_parameters
from mutwo import core_utilities
from mutwo import music_parameters

__all__ = (
    "PitchInterval",
    "Pitch",
    "Volume",
    "PitchAmbitus",
    "PlayingIndicator",
    "NotationIndicator",
    "Lyric",
    "Syllable",
    "Instrument",
    "PitchedInstrument",
)


class PitchInterval(
    core_parameters.abc.SingleNumberParameter,
    value_name="cents",
    value_return_type=float,
):
    """Abstract base class for any pitch interval class

    If the user wants to define a new pitch interval class, the abstract
    property :attr:`cents` and the abstract method `inverse`
    have to be overridden.

    See `wikipedia entry <https://en.wikipedia.org/wiki/Cent_(music)>`_
    for definition of 'cents'.
    """

    Type: typing.TypeAlias = typing.Union[float, int, str, "PitchInterval"]

    def __repr__(self) -> str:
        return str(self)

    @abc.abstractmethod
    def inverse(self) -> PitchInterval:
        """Makes falling interval to rising and vice versa.

        In `music21` the method for equal semantics is called
        `reverse <https://web.mit.edu/music21/doc/moduleReference/moduleInterval.html#music21.interval.Interval.reverse>`_.
        """

    def __add__(self, other: PitchInterval) -> PitchInterval:
        return music_parameters.DirectPitchInterval(self.cents + other.cents)

    def __sub__(self, other: PitchInterval) -> PitchInterval:
        return music_parameters.DirectPitchInterval(self.cents - other.cents)

    @classmethod
    def from_any(cls, object: PitchInterval.Type) -> PitchInterval:
        match object:
            case PitchInterval():
                return object
            case int() | float():
                return music_parameters.DirectPitchInterval(object)
            case str():
                if "/" in object:
                    return music_parameters.JustIntonationPitch(object)
                try:
                    return music_parameters.WesternPitchInterval(object)
                except Exception:
                    f = core_utilities.str_to_number_parser(object)
                    try:
                        v = f(object)
                    except ValueError:
                        pass
                    else:
                        return cls.from_any(v)
            case _:
                pass
        raise core_utilities.CannotParseError(object, cls)


class Pitch(
    core_parameters.abc.SingleNumberParameter,
    value_name="hertz",
    value_return_type=float,
):
    """Abstract base class for any pitch class.

    If the user wants to define a new pitch class, the abstract
    property :attr:`hertz` has to be overridden. Starting
    from mutwo version = 0.46.0 the user will furthermore have
    to define an :func:`add` method.
    """

    Type: typing.TypeAlias = typing.Union[fractions.Fraction, float, int, str, "Pitch"]
    """Pitch.Type hosts all types that are supported by the pitch parser
    :func:`Pitch.from_any`."""

    # ###################################################################### #
    #     conversion methods between different pitch describing units        #
    # ###################################################################### #

    @staticmethod
    def hertz_to_cents(
        frequency0: core_constants.Real, frequency1: core_constants.Real
    ) -> float:
        """Calculates the difference in cents between two frequencies.

        :param frequency0: The first frequency in Hertz.
        :param frequency1: The second frequency in Hertz.
        :return: The difference in cents between the first and the second
            frequency.

        **Example:**

        >>> from mutwo import music_parameters
        >>> music_parameters.abc.Pitch.hertz_to_cents(200, 400)
        1200.0
        """
        return float(1200 * math.log(frequency1 / frequency0, 2))

    @staticmethod
    def ratio_to_cents(ratio: fractions.Fraction) -> float:
        """Converts a frequency ratio to its respective cent value.

        :param ratio: The frequency ratio which cent value shall be
            calculated.

        **Example:**

        >>> from mutwo import music_parameters
        >>> music_parameters.abc.Pitch.ratio_to_cents(fractions.Fraction(3, 2))
        701.9550008653874
        """
        return music_parameters.constants.CENT_CALCULATION_CONSTANT * math.log10(ratio)

    @staticmethod
    def cents_to_ratio(cents: core_constants.Real) -> fractions.Fraction:
        """Converts a cent value to its respective frequency ratio.

        :param cents: Cents that shall be converted to a frequency ratio.

        **Example:**

        >>> from mutwo import music_parameters
        >>> music_parameters.abc.Pitch.cents_to_ratio(1200)
        Fraction(2, 1)
        """
        return fractions.Fraction(
            10 ** (cents / music_parameters.constants.CENT_CALCULATION_CONSTANT)
        )

    @staticmethod
    def hertz_to_midi_pitch_number(frequency: core_constants.Real) -> float:
        """Converts a frequency in hertz to its respective midi pitch.

        :param frequency: The frequency that shall be translated to a midi pitch
            number.
        :return: The midi pitch number (potentially a floating point number if the
            entered frequency isn't on the grid of the equal divided octave tuning
            with a = 440 Hertz).

        **Example:**

        >>> from mutwo import music_parameters
        >>> music_parameters.abc.Pitch.hertz_to_midi_pitch_number(440)
        69.0
        >>> music_parameters.abc.Pitch.hertz_to_midi_pitch_number(440 * 3 / 2)
        75.98044999134612
        """
        closest_frequency_index = core_utilities.find_closest_index(
            frequency, music_parameters.constants.MIDI_PITCH_FREQUENCY_TUPLE
        )
        closest_frequency = music_parameters.constants.MIDI_PITCH_FREQUENCY_TUPLE[
            closest_frequency_index
        ]
        closest_midi_pitch_number = music_parameters.constants.MIDI_PITCH_NUMBER_TUPLE[
            closest_frequency_index
        ]
        difference_in_cents = Pitch.hertz_to_cents(frequency, closest_frequency)
        return float(closest_midi_pitch_number + (difference_in_cents / 100))

    # ###################################################################### #
    #                            class methods                               #
    # ###################################################################### #

    @classmethod
    def from_any(cls, object: Pitch.Type) -> Pitch:
        builtin_fraction = _fractions.Fraction if _fractions else fractions.Fraction
        match object:
            case music_parameters.abc.Pitch():
                return object
            case str():
                if "/" in object:  # assumes it is a ratio
                    return music_parameters.JustIntonationPitch(object)
                elif (  # assumes it is a WesternPitch name
                    object[0]
                    in music_parameters.constants.DIATONIC_PITCH_CLASS_CONTAINER
                ):
                    if object[-1].isdigit():
                        pitch_name, octave = object[:-1], int(object[-1])
                        return music_parameters.WesternPitch(pitch_name, octave)
                    else:
                        return music_parameters.WesternPitch(object)
                else:  # assume it's a number in a string
                    try:
                        v = ast.literal_eval(object)
                    except Exception:
                        pass  # raise CannotParseError
                    else:
                        return cls.from_any(v)
            case fractions.Fraction() | builtin_fraction():
                return music_parameters.JustIntonationPitch(object)
            case float() | int():
                return music_parameters.DirectPitch(object)
            case list() | tuple():
                return music_parameters.FlexPitch(object)
            case _:
                pass

        raise core_utilities.CannotParseError(object, cls)

    # ###################################################################### #
    #                            public properties                           #
    # ###################################################################### #

    @property
    def midi_pitch_number(self) -> float:
        """The midi pitch number (from 0 to 127) of the pitch."""
        return self.hertz_to_midi_pitch_number(self.hertz)

    # ###################################################################### #
    #                            comparison methods                          #
    # ###################################################################### #

    @abc.abstractmethod
    def add(self, pitch_interval: PitchInterval.Type) -> Pitch: ...

    def subtract(
        self, pitch_interval: music_parameters.abc.PitchInterval.Type
    ) -> Pitch:
        return self.add(PitchInterval.from_any(pitch_interval).inverse())

    def __add__(self, pitch_interval: PitchInterval.Type) -> Pitch:
        return self.copy().add(pitch_interval)

    def __sub__(self, pitch_interval: PitchInterval.Type) -> Pitch:
        return self.copy().subtract(pitch_interval)

    def get_pitch_interval(self, pitch_to_compare: Pitch) -> PitchInterval:
        """Get :class:`PitchInterval` between itself and other pitch

        :param pitch_to_compare: The pitch which shall be compared to
            the active pitch.
        :type pitch_to_compare: Pitch
        :return: :class:`PitchInterval` between

        **Example:**

        >>> from mutwo import music_parameters
        >>> a4 = music_parameters.DirectPitch(hertz=440)
        >>> a5 = music_parameters.DirectPitch(hertz=880)
        >>> pitch_interval = a4.get_pitch_interval(a5)
        """

        cent_difference = self.ratio_to_cents(pitch_to_compare.hertz / self.hertz)
        return music_parameters.DirectPitchInterval(cent_difference)


class PitchList(core_parameters.abc.Parameter, list[Pitch]):
    """PitchList provides functionality to parse objects to a list of pitches"""

    Type: typing.TypeAlias = typing.Union[
        Pitch.Type, list[Pitch], tuple[Pitch], str, types.NoneType
    ]
    """PitchList.Type hosts all types that are supported by the pitch
    list parser :func:`PitchList.from_any`."""

    @classmethod
    def from_any(cls, object: Pitch.Type) -> Pitch:
        match object:
            case None:
                return []
            case list() | tuple():
                return [Pitch.from_any(p) for p in object]
            case str():
                return [
                    Pitch.from_any(pitch_indication)
                    for pitch_indication in object.split(" ")
                    if pitch_indication
                ]
            case _:
                return [Pitch.from_any(object)]


@functools.total_ordering  # type: ignore
class Volume(
    core_parameters.abc.SingleNumberParameter,
    value_name="decibel",
    value_return_type=float,
):
    """Abstract base class for any volume class.

    If the user wants to define a new volume class, the abstract
    property :attr:`decibel` has to be overridden.
    """

    Type: typing.TypeAlias = typing.Union[core_constants.Real, str, "Volume"]
    """Volume.Type hosts all types that are supported by the volume parser
    :func:`Volume.from_any`."""

    @staticmethod
    def decibel_to_amplitude_ratio(
        decibel: core_constants.Real, reference_amplitude: core_constants.Real = 1
    ) -> float:
        """Convert decibel to amplitude ratio.

        :param decibel: The decibel number that shall be converted.
        :param reference_amplitude: The amplitude for decibel == 0.

        **Example:**

        >>> from mutwo import music_parameters
        >>> music_parameters.abc.Volume.decibel_to_amplitude_ratio(0)
        1.0
        >>> music_parameters.abc.Volume.decibel_to_amplitude_ratio(-6)
        0.5011872336272722
        >>> music_parameters.abc.Volume.decibel_to_amplitude_ratio(0, reference_amplitude=0.25)
        0.25
        """
        return float(reference_amplitude * (10 ** (decibel / 20)))

    @staticmethod
    def decibel_to_power_ratio(
        decibel: core_constants.Real, reference_amplitude: core_constants.Real = 1
    ) -> float:
        """Convert decibel to power ratio.

        :param decibel: The decibel number that shall be converted.
        :param reference_amplitude: The amplitude for decibel == 0.

        **Example:**

        >>> from mutwo import music_parameters
        >>> music_parameters.abc.Volume.decibel_to_power_ratio(0)
        1.0
        >>> music_parameters.abc.Volume.decibel_to_power_ratio(-6)
        0.251188643150958
        >>> music_parameters.abc.Volume.decibel_to_power_ratio(0, reference_amplitude=0.25)
        0.25
        """
        return float(reference_amplitude * (10 ** (decibel / 10)))

    @staticmethod
    def amplitude_ratio_to_decibel(
        amplitude: core_constants.Real, reference_amplitude: core_constants.Real = 1
    ) -> float:
        """Convert amplitude ratio to decibel.

        :param amplitude: The amplitude that shall be converted.
        :param reference_amplitude: The amplitude for decibel == 0.

        **Example:**

        >>> from mutwo import music_parameters
        >>> music_parameters.abc.Volume.amplitude_ratio_to_decibel(1)
        0.0
        >>> music_parameters.abc.Volume.amplitude_ratio_to_decibel(0)
        -inf
        >>> music_parameters.abc.Volume.amplitude_ratio_to_decibel(0.5)
        -6.020599913279624
        """
        if amplitude == 0:
            return float("-inf")
        else:
            return float(20 * math.log10(amplitude / reference_amplitude))

    @staticmethod
    def power_ratio_to_decibel(
        amplitude: core_constants.Real, reference_amplitude: core_constants.Real = 1
    ) -> float:
        """Convert power ratio to decibel.

        :param amplitude: The amplitude that shall be converted.
        :param reference_amplitude: The amplitude for decibel == 0.

        **Example:**

        >>> from mutwo import music_parameters
        >>> music_parameters.abc.Volume.power_ratio_to_decibel(1)
        0.0
        >>> music_parameters.abc.Volume.power_ratio_to_decibel(0)
        -inf
        >>> music_parameters.abc.Volume.power_ratio_to_decibel(0.5)
        -3.010299956639812
        """
        if amplitude == 0:
            return float("-inf")
        else:
            return float(10 * math.log10(amplitude / reference_amplitude))

    @staticmethod
    def amplitude_ratio_to_midi_velocity(
        amplitude: core_constants.Real, reference_amplitude: core_constants.Real = 1
    ) -> int:
        """Convert amplitude ratio to midi velocity.

        :param amplitude: The amplitude which shall be converted.
        :type amplitude: core_constants.Real
        :param reference_amplitude: The amplitude for decibel == 0.
        :return: The midi velocity.

        The method clips values that are higher than 1 / lower than 0.

        **Example:**

        >>> from mutwo import music_parameters
        >>> music_parameters.abc.Volume.amplitude_ratio_to_midi_velocity(1)
        127
        >>> music_parameters.abc.Volume.amplitude_ratio_to_midi_velocity(0)
        0
        """

        return Volume.decibel_to_midi_velocity(
            Volume.amplitude_ratio_to_decibel(
                amplitude, reference_amplitude=reference_amplitude
            )
        )

    @staticmethod
    def decibel_to_midi_velocity(
        decibel_to_convert: core_constants.Real,
        minimum_decibel: typing.Optional[core_constants.Real] = None,
        maximum_decibel: typing.Optional[core_constants.Real] = None,
    ) -> int:
        """Convert decibel to midi velocity (0 to 127).

        :param decibel: The decibel value which shall be converted..
        :type decibel: core_constants.Real
        :param minimum_decibel: The decibel value which is equal to the lowest
            midi velocity (0).
        :type minimum_decibel: core_constants.Real, optional
        :param maximum_decibel: The decibel value which is equal to the highest
            midi velocity (127).
        :type maximum_decibel: core_constants.Real, optional
        :return: The midi velocity.

        The method clips values which are higher than 'maximum_decibel' and lower than
        'minimum_decibel'.

        **Example:**

        >>> from mutwo import music_parameters
        >>> music_parameters.abc.Volume.decibel_to_midi_velocity(0)
        127
        >>> music_parameters.abc.Volume.decibel_to_midi_velocity(-40)
        0
        """

        minimum_decibel = (
            minimum_decibel
            or music_parameters.configurations.DEFAULT_MINIMUM_DECIBEL_FOR_MIDI_VELOCITY_AND_STANDARD_DYNAMIC_INDICATOR
        )
        maximum_decibel = (
            maximum_decibel
            or music_parameters.configurations.DEFAULT_MAXIMUM_DECIBEL_FOR_MIDI_VELOCITY_AND_STANDARD_DYNAMIC_INDICATOR
        )

        if decibel_to_convert > maximum_decibel:
            decibel_to_convert = maximum_decibel

        if decibel_to_convert < minimum_decibel:
            decibel_to_convert = minimum_decibel

        velocity = int(
            core_utilities.scale(
                decibel_to_convert,
                minimum_decibel,
                maximum_decibel,
                music_parameters.constants.MINIMUM_VELOCITY,
                music_parameters.constants.MAXIMUM_VELOCITY,
            )
        )

        return velocity

    @classmethod
    def from_any(cls, object: Volume.Type) -> Volume:
        match object:
            case music_parameters.abc.Volume():
                return object
            case numbers.Real():
                return music_parameters.DirectVolume(object)  # type: ignore
            case str():
                if object in music_parameters.constants.DYNAMIC_INDICATOR_TUPLE:
                    return music_parameters.WesternVolume(object)
                else:
                    try:
                        v = ast.literal_eval(object)
                    except Exception:
                        pass  # raise CannotParseError
                    else:
                        return cls.from_any(v)
            case list() | tuple():
                return music_parameters.FlexVolume(object)
            case _:
                pass
        raise core_utilities.CannotParseError(object, cls)

    # properties
    @property
    def amplitude(self) -> core_constants.Real:
        return self.decibel_to_amplitude_ratio(self.decibel)

    @property
    def midi_velocity(self) -> int:
        """The velocity of the volume (from 0 to 127)."""
        return self.decibel_to_midi_velocity(self.decibel)


class PitchAmbitus(core_parameters.abc.Parameter):
    """Abstract base class for all pitch ambituses.

    To setup a new PitchAmbitus class override the abstract method
    `pitch_to_period`.
    """

    def __init__(self, minima_pitch: Pitch, maxima_pitch: Pitch) -> None:
        try:
            assert minima_pitch < maxima_pitch
        except AssertionError:
            raise ValueError(
                (
                    f"Found minima_pitch: {minima_pitch} and "
                    f"maxima_pitch={maxima_pitch}. The minima pitch has to be "
                    "a lower pitch than the maxima pitch!"
                )
            )

        self.minima_pitch = minima_pitch
        self.maxima_pitch = maxima_pitch

    # ######################################################## #
    #                      abstract methods                    #
    # ######################################################## #

    @abc.abstractmethod
    def pitch_to_period(self, pitch: Pitch) -> PitchInterval: ...

    # ######################################################## #
    #                     magic methods                        #
    # ######################################################## #

    def __repr__(self) -> str:
        return f"{type(self).__name__}{self.border_tuple}"

    def __str__(self) -> str:
        return repr(self)

    def __iter__(self) -> typing.Iterator[Pitch]:
        return iter(self.border_tuple)

    def __getitem__(self, index: int) -> Pitch:
        return self.border_tuple[index]

    def __contains__(self, pitch: typing.Any) -> bool:
        return bool(self.filter_pitch_sequence((pitch,)))

    # ######################################################## #
    #                       properties                         #
    # ######################################################## #

    @property
    def border_tuple(self) -> tuple[Pitch, Pitch]:
        return (self.minima_pitch, self.maxima_pitch)

    @property
    def range(self) -> PitchInterval:
        return self.minima_pitch.get_pitch_interval(self.maxima_pitch)

    # ######################################################## #
    #                       public methods                     #
    # ######################################################## #

    def get_pitch_variant_tuple(
        self, pitch: Pitch, period: typing.Optional[PitchInterval] = None
    ) -> tuple[Pitch, ...]:
        """Find all pitch variants (in all octaves) of the given pitch

        :param pitch: The pitch which variants shall be found.
        :type pitch: Pitch
        :param period: The repeating period (usually an octave). If the
            period is set to `None` the function will fallback to them
            objects method :meth:`PitchAmbitus.pitch_to_period`. Default to `None`.
        :type period: typing.Optional[PitchInterval]
        """

        period = period or self.pitch_to_period(pitch)
        pitch_variant_list = []

        is_first = True
        for loop_condition, append_condition, change_pitch in (
            (
                lambda dummy_pitch: dummy_pitch <= self.maxima_pitch,
                lambda dummy_pitch: dummy_pitch >= self.minima_pitch,
                lambda dummy_pitch: dummy_pitch.add(period),
            ),
            (
                lambda dummy_pitch: dummy_pitch >= self.minima_pitch,
                lambda dummy_pitch: dummy_pitch <= self.maxima_pitch,
                lambda dummy_pitch: dummy_pitch.subtract(period),
            ),
        ):
            dummy_pitch = copy.copy(pitch)
            if not is_first:
                change_pitch(dummy_pitch)
            while loop_condition(dummy_pitch):
                if append_condition(dummy_pitch):
                    pitch_variant_list.append(copy.copy(dummy_pitch))
                change_pitch(dummy_pitch)
            is_first = False

        return tuple(sorted(pitch_variant_list))

    def filter_pitch_sequence(
        self,
        pitch_to_filter_sequence: typing.Sequence[Pitch],
    ) -> tuple[Pitch, ...]:
        """Filter all pitches in a sequence which aren't inside the ambitus.

        :param pitch_to_filter_sequence: A sequence with pitches which shall
            be filtered.
        :type pitch_to_filter_sequence: typing.Sequence[Pitch]

        **Example:**

        >>> from mutwo import music_parameters
        >>> ambitus0 = music_parameters.OctaveAmbitus(
        ...     music_parameters.JustIntonationPitch('1/2'),
        ...     music_parameters.JustIntonationPitch('2/1'),
        ... )
        >>> ambitus0.filter_pitch_sequence(
        ...     [
        ...         music_parameters.JustIntonationPitch("3/8"),
        ...         music_parameters.JustIntonationPitch("3/4"),
        ...         music_parameters.JustIntonationPitch("3/2"),
        ...         music_parameters.JustIntonationPitch("3/1"),
        ...     ]
        ... )
        (JustIntonationPitch('3/4'), JustIntonationPitch('3/2'))
        """

        return tuple(
            filter(
                lambda pitch: pitch >= self.minima_pitch and pitch <= self.maxima_pitch,
                pitch_to_filter_sequence,
            )
        )


@dataclasses.dataclass()  # type: ignore
class Indicator(core_parameters.abc.Parameter):
    @property
    @abc.abstractmethod
    def is_active(self) -> bool: ...

    def get_arguments_dict(self) -> dict[str, typing.Any]:
        return {
            key: getattr(self, key)
            for key in self.__dataclass_fields__.keys()  # type: ignore
        }


class PlayingIndicator(Indicator):
    """Abstract base class for any playing indicator."""


class ExplicitPlayingIndicator(PlayingIndicator):
    def __init__(self, is_active: bool = False):
        self.is_active = is_active

    def __repr__(self):
        return "{}({})".format(type(self).__name__, self.is_active)

    def get_arguments_dict(self) -> dict[str, typing.Any]:
        return {"is_active": self.is_active}

    @property
    def is_active(self) -> bool:
        return self._is_active

    @is_active.setter
    def is_active(self, is_active: bool):
        self._is_active = is_active


@dataclasses.dataclass()
class ImplicitPlayingIndicator(PlayingIndicator):
    @property
    def is_active(self) -> bool:
        return all(
            tuple(
                argument is not None for argument in self.get_arguments_dict().values()
            )
        )


class NotationIndicator(Indicator):
    """Abstract base class for any notation indicator."""

    @property
    def is_active(self) -> bool:
        return all(
            tuple(
                argument is not None for argument in self.get_arguments_dict().values()
            )
        )


T = typing.TypeVar("T", PlayingIndicator, NotationIndicator)


class IndicatorCollection(core_parameters.abc.Parameter, typing.Generic[T]):
    """An :class:`IndicatorCollection` hosts a collection of indicators."""

    Type: typing.TypeAlias = typing.Union[types.NoneType, str, "IndicatorCollection"]
    """IndicatorCollection.Type hosts all types that are supported by the indicator
    collection parser :func:`IndicatorCollection.from_any`."""

    def __init_subclass__(cls):
        # This makes sure, that we only register indicators at the class
        # itself, but not at other classes (e.g. its super class or other
        # sub classes of the same super class). It also makes sure that when
        # we inherit from a 'IndicatorCollection', we also inherit all already
        # registered indicators.
        IndicatorName: typing.TypeAlias = str
        cls._indicator_type_dict: dict[IndicatorName, typing.Type[Indicator]] = dict(
            getattr(cls, "_indicator_type_dict", {})
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for key, factory in self._indicator_type_dict.items():
            setattr(self, key, factory())

    def __eq__(self, other: typing.Any):
        try:
            indicator_dict1 = other.indicator_dict
        except AttributeError:
            return False

        indicator_dict0 = self.indicator_dict

        # Ensure we have the same indicators in both collections
        key_set0 = set(indicator_dict0.keys())
        key_set1 = set(indicator_dict1.keys())
        if key_set0.difference(key_set1):
            return False

        # Finally compare all indicators themselves and check if they
        # have the same values
        for k in indicator_dict0.keys():
            if indicator_dict0[k] != indicator_dict1[k]:
                return False

        return True

    @property
    def indicator_tuple(self) -> tuple[T, ...]:
        return tuple(getattr(self, key) for key in self._indicator_type_dict.keys())

    @property
    def indicator_dict(self) -> dict[str, Indicator]:
        return {key: getattr(self, key) for key in self._indicator_type_dict.keys()}

    @classmethod
    def from_any(cls, object: IndicatorCollection.Type) -> IndicatorCollection:
        from mutwo import music_utilities

        match object:
            case None:
                return cls()
            case cls():
                return object
            case str():
                return music_utilities.IndicatorCollectionParser().parse(object, cls())
            case _:
                raise core_utilities.CannotParseError(object, cls)

    @classmethod
    def register(
        cls, indicator: typing.Type[Indicator], name: typing.Optional[str] = None
    ):
        """Register new indicator type to collection.

        :param indicator: The indicator type that is registered.
        :type indicator: typing.Type[Indicator]
        :param name: The attribute name of the collection that points to
            the indicator. If `None` this is automatically set to a lower
            snake case version of the type name (e.g. 'MarginMarkup' is
            converted to 'margin_markup'). Default to `None`.
        :type name: typing.Optional[str] = None
        """
        name = name or core_utilities.camel_case_to_snake_case(indicator.__name__)
        cls._indicator_type_dict[name] = indicator
        return indicator


class Lyric(
    core_parameters.abc.SingleValueParameter,
    value_name="xsampa",
    value_return_type=str,
):
    """Abstract base class for any spoken, sung or written text.

    If the user wants to define a new lyric class, the abstract
    properties :attr:`xampa` and
    :attr:`written_representation` have to be overridden.

    The :attr:`xsampa` should return a string of
    X-SAMPA format phonemes, separated by space to indicate new words.
    Consult `wikipedia entry <https://en.wikipedia.org/wiki/X-SAMPA>`_
    for detailed information regarding X-SAMPA.

    The :attr:`written_representation` should return a string of
    normal written text, separated by space to indicate new words.
    """

    @property
    def written_representation(self) -> str:
        """Get text as it would be written in natural language"""


class Syllable(Lyric):
    """Syllable mixin for classes which inherit from :class:`Lyric`.

    This adds the new attribute :attr:`is_last_syllable`. This should
    be `True` if it is the last syllable of a word and `False` if it
    isn't.
    """

    def __init__(self, is_last_syllable: bool):
        self.is_last_syllable = is_last_syllable


@dataclasses.dataclass(frozen=True)
class Instrument(core_parameters.abc.Parameter):
    """Model a musical instrument.

    :param name: The name of the instrument.
    :type name: str
    :param short_name: The abbreviation of the instrument.
        If set to ``None`` it will be the same like `name`.
        Default to ``None``.
    :type short_name: typing.Optional[str]

    This is an abstract class. To create a new concrete class
    you need to override the abstract `is_pitched` property.
    Alternatively you can use the ready-to-go classes
    :class:`mutwo.music_parameters.UnpitchedInstrument` or
    :class:`mutwo.music_parameters.ContinuousPitchedInstrument` or
    :class:`mutwo.music_parameters.DiscreetPitchedInstrument`.
    """

    name: str
    short_name: typing.Optional[str] = None

    def __post_init__(self):
        # Auto set short_name to name if not declared
        object.__setattr__(self, "short_name", self.short_name or self.name)

    @property
    @abc.abstractmethod
    def is_pitched(self) -> bool:
        """Return ``True`` if instrument is pitched, ``False`` otherwise."""


@dataclasses.dataclass(frozen=True)
class PitchedInstrument(Instrument):
    """Model a pitched musical instrument.

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

    You can use pythons `in` syntax to find out if a pitch
    is playable by the given instrument.

    This is an abstract class. You need to override abstract
    method `__contains__` and abstract property `pitch_ambitus`.
    """

    pitch_count_range: ranges.Range = ranges.Range(1, 2)
    transposition_pitch_interval: typing.Optional[
        music_parameters.abc.DirectPitchInterval
    ] = None

    def __post_init__(self):
        super().__post_init__()
        object.__setattr__(
            self,
            "transposition_pitch_interval",
            music_parameters.DirectPitchInterval(0),
        )

    @abc.abstractmethod
    def __contains__(self, pitch: typing.Any) -> bool: ...

    @property
    @abc.abstractmethod
    def pitch_ambitus(self) -> music_parameters.abc.PitchAmbitus: ...

    @property
    def is_pitched(self) -> bool:
        return True

    @abc.abstractmethod
    def get_pitch_variant_tuple(
        self, pitch: Pitch, period: typing.Optional[PitchInterval] = None
    ) -> tuple[Pitch, ...]:
        """Find all pitch variants (in all octaves) of the given pitch

        :param pitch: The pitch which variants shall be found.
        :type pitch: Pitch
        :param period: The repeating period (usually an octave). If the
            period is set to `None` the function will fallback to them
            objects method :meth:`PitchAmbitus.pitch_to_period`. Default to `None`.
        :type period: typing.Optional[PitchInterval]

        This is not necessarily the same as
        ``instrument.pitch_ambitus.get_pitch_variant_tuple()``, because
        a :class:`mutwo.music_parameters.DiscreetPitchedInstrument` may
        not be capable of playing a pitch even if the given pitch is within
        the ambitus of an instrument. It's therefore recommended to
        use ``instrument.get_pitch_variant_tuple`` if one wants to find
        out in which octaves the given pitch is actually playable on the
        instrument.
        """
