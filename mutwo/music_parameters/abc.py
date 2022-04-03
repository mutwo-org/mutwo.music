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
import copy
import dataclasses
import functools
import math
import typing

try:
    import quicktions as fractions  # type: ignore
except ImportError:
    import fractions  # type: ignore

from mutwo import core_constants
from mutwo import core_events
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
)


class PitchInterval(
    core_parameters.abc.SingleNumberParameter,
    value_name="interval",
    value_return_type=float,
):
    """Abstract base class for any pitch interval class

    If the user wants to define a new pitch interval class, the abstract
    property :attr:`interval` has to be overridden.

    :attr:`interval` is stored in unit `cents`.

    See `wikipedia entry <https://en.wikipedia.org/wiki/Cent_(music)>`_
    for definition of 'cents'.
    """

    pass


class Pitch(
    core_parameters.abc.SingleNumberParameter,
    core_parameters.abc.ParameterWithEnvelope,
    value_name="frequency",
    value_return_type=float,
):
    """Abstract base class for any pitch class.

    If the user wants to define a new pitch class, the abstract
    property :attr:`frequency` has to be overridden. Starting
    from mutwo version = 0.46.0 the user will furthermore have
    to define an :func:`add` and a :func:`subtract` method.
    """

    class PitchEnvelope(core_events.Envelope):
        """Default resolution envelope class for :class:`Pitch`"""

        def __init__(
            self,
            *args,
            event_to_parameter: typing.Optional[
                typing.Callable[[core_events.abc.Event], core_constants.ParameterType]
            ] = None,
            value_to_parameter: typing.Optional[
                typing.Callable[
                    [core_events.Envelope.Value], core_constants.ParameterType
                ]
            ] = None,
            parameter_to_value: typing.Optional[
                typing.Callable[
                    [core_constants.ParameterType], core_events.Envelope.Value
                ]
            ] = None,
            apply_parameter_on_event: typing.Optional[
                typing.Callable[
                    [core_events.abc.Event, core_constants.ParameterType], None
                ]
            ] = None,
            **kwargs,
        ):
            if not event_to_parameter:
                event_to_parameter = self._event_to_parameter
            if not value_to_parameter:
                value_to_parameter = self._value_to_parameter
            if not apply_parameter_on_event:
                apply_parameter_on_event = self._apply_parameter_on_event
            if not parameter_to_value:
                parameter_to_value = self._parameter_to_value

            super().__init__(
                *args,
                event_to_parameter=event_to_parameter,
                value_to_parameter=value_to_parameter,
                parameter_to_value=parameter_to_value,
                apply_parameter_on_event=apply_parameter_on_event,
                **kwargs,
            )

        @classmethod
        def frequency_and_envelope_to_pitch(
            cls,
            frequency: core_constants.Real,
            envelope: typing.Optional[
                typing.Union[Pitch.PitchIntervalEnvelope, typing.Sequence]
            ] = None,
        ) -> Pitch:
            return music_parameters.DirectPitch(frequency, envelope=envelope)

        @classmethod
        def _value_to_parameter(
            cls,
            value: core_events.Envelope.Value,  # type: ignore
        ) -> core_constants.ParameterType:
            # For inner calculation (value) cents are used instead
            # of frequencies. In this way we can ensure that the transitions
            # are closer to the human logarithmic hearing.
            # See als `_parameter_to_value`.
            frequency = (
                Pitch.cents_to_ratio(value)
                * music_parameters.constants.PITCH_ENVELOPE_REFERENCE_FREQUENCY
            )
            return cls.frequency_and_envelope_to_pitch(frequency)

        @classmethod
        def _event_to_parameter(
            cls, event: core_events.abc.Event
        ) -> core_constants.ParameterType:
            if hasattr(
                event,
                music_parameters.configurations.DEFAULT_PITCH_ENVELOPE_PARAMETER_NAME,
            ):
                return getattr(
                    event,
                    music_parameters.configurations.DEFAULT_PITCH_ENVELOPE_PARAMETER_NAME,
                )
            else:
                return cls.frequency_and_envelope_to_pitch(
                    music_parameters.configurations.DEFAULT_CONCERT_PITCH
                )

        @classmethod
        def _apply_parameter_on_event(
            cls, event: core_events.abc.Event, parameter: core_constants.ParameterType
        ):
            setattr(
                event,
                music_parameters.configurations.DEFAULT_PITCH_ENVELOPE_PARAMETER_NAME,
                parameter,
            )

        @classmethod
        def _parameter_to_value(
            cls, parameter: core_constants.ParameterType
        ) -> core_constants.Real:
            # For inner calculation (value) cents are used instead
            # of frequencies. In this way we can ensure that the transitions
            # are closer to the human logarithmic hearing.
            # See als `_value_to_parameter`.
            return Pitch.hertz_to_cents(
                music_parameters.constants.PITCH_ENVELOPE_REFERENCE_FREQUENCY,
                parameter.frequency,
            )

    class PitchIntervalEnvelope(core_events.RelativeEnvelope):
        """Default envelope class for :class:`Pitch`

        Resolves into :class:`Pitch.PitchEnvelope`.
        """

        def __init__(
            self,
            *args,
            event_to_parameter: typing.Optional[
                typing.Callable[[core_events.abc.Event], core_constants.ParameterType]
            ] = None,
            value_to_parameter: typing.Optional[
                typing.Callable[
                    [core_events.Envelope.Value], core_constants.ParameterType
                ]
            ] = None,
            parameter_to_value: typing.Callable[
                [core_constants.ParameterType], core_events.Envelope.Value
            ] = lambda parameter: parameter.interval,
            apply_parameter_on_event: typing.Optional[
                typing.Callable[
                    [core_events.abc.Event, core_constants.ParameterType], None
                ]
            ] = None,
            base_parameter_and_relative_parameter_to_absolute_parameter: typing.Optional[
                typing.Callable[
                    [core_constants.ParameterType, core_constants.ParameterType],
                    core_constants.ParameterType,
                ]
            ] = None,
            **kwargs,
        ):
            if not event_to_parameter:
                event_to_parameter = self._event_to_parameter
            if not value_to_parameter:
                value_to_parameter = self._value_to_parameter
            if not apply_parameter_on_event:
                apply_parameter_on_event = self._apply_parameter_on_event
            if not base_parameter_and_relative_parameter_to_absolute_parameter:
                base_parameter_and_relative_parameter_to_absolute_parameter = (
                    self._base_parameter_and_relative_parameter_to_absolute_parameter
                )

            super().__init__(
                *args,
                event_to_parameter=event_to_parameter,
                value_to_parameter=value_to_parameter,
                parameter_to_value=parameter_to_value,
                apply_parameter_on_event=apply_parameter_on_event,
                base_parameter_and_relative_parameter_to_absolute_parameter=base_parameter_and_relative_parameter_to_absolute_parameter,
                **kwargs,
            )

        @classmethod
        def cents_to_pitch_interval(cls, cents: core_constants.Real) -> PitchInterval:
            return music_parameters.DirectPitchInterval(cents)

        @classmethod
        def _event_to_parameter(
            cls, event: core_events.abc.Event
        ) -> core_constants.ParameterType:
            if hasattr(
                event,
                music_parameters.configurations.DEFAULT_PITCH_INTERVAL_ENVELOPE_PARAMETER_NAME,
            ):
                return getattr(
                    event,
                    music_parameters.configurations.DEFAULT_PITCH_INTERVAL_ENVELOPE_PARAMETER_NAME,
                )
            else:
                return cls.cents_to_pitch_interval(0)

        @classmethod
        def _value_to_parameter(
            cls, value: core_events.Envelope.Value
        ) -> core_constants.ParameterType:
            return cls.cents_to_pitch_interval(value)

        @classmethod
        def _apply_parameter_on_event(
            cls, event: core_events.abc.Event, parameter: core_constants.ParameterType
        ):
            setattr(
                event,
                music_parameters.configurations.DEFAULT_PITCH_INTERVAL_ENVELOPE_PARAMETER_NAME,
                parameter,
            ),

        @classmethod
        def _base_parameter_and_relative_parameter_to_absolute_parameter(
            cls, base_parameter: Pitch, relative_parameter: PitchInterval
        ) -> Pitch:
            return base_parameter + relative_parameter

    def __init__(
        self,
        envelope: typing.Optional[
            typing.Union[Pitch.PitchIntervalEnvelope, typing.Sequence]
        ] = None,
    ):
        self.envelope = envelope

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

        >>> from mutwo.parameters import abc
        >>> abc.Pitch.hertz_to_cents(200, 400)
        1200.0
        """
        return float(1200 * math.log(frequency1 / frequency0, 2))

    @staticmethod
    def ratio_to_cents(ratio: fractions.Fraction) -> float:
        """Converts a frequency ratio to its respective cent value.

        :param ratio: The frequency ratio which cent value shall be
            calculated.

        **Example:**

        >>> from mutwo.parameters import abc
        >>> abc.Pitch.ratio_to_cents(fractions.Fraction(3, 2))
        701.9550008653874
        """
        return music_parameters.constants.CENT_CALCULATION_CONSTANT * math.log10(ratio)

    @staticmethod
    def cents_to_ratio(cents: core_constants.Real) -> fractions.Fraction:
        """Converts a cent value to its respective frequency ratio.

        :param cents: Cents that shall be converted to a frequency ratio.

        **Example:**

        >>> from mutwo.parameters import abc
        >>> abc.Pitch.cents_to_ratio(1200)
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

        >>> from mutwo.parameters import abc
        >>> abc.Pitch.hertz_to_midi_pitch_number(440)
        69.0
        >>> abc.Pitch.hertz_to_midi_pitch_number(440 * 3 / 2)
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
    #                            public properties                           #
    # ###################################################################### #

    @property
    def midi_pitch_number(self) -> float:
        """The midi pitch number (from 0 to 127) of the pitch."""
        return self.hertz_to_midi_pitch_number(self.frequency)

    @core_parameters.abc.ParameterWithEnvelope.envelope.setter
    def envelope(
        self,
        envelope_or_envelope_argument: typing.Optional[
            typing.Union[Pitch.PitchIntervalEnvelope, typing.Sequence]
        ],
    ):
        if not envelope_or_envelope_argument:
            generic_pitch_interval = self.PitchIntervalEnvelope.cents_to_pitch_interval(
                0
            )
            envelope = self.PitchIntervalEnvelope([[0, generic_pitch_interval]])
        elif isinstance(envelope_or_envelope_argument, core_events.RelativeEnvelope):
            envelope = envelope_or_envelope_argument
        else:
            envelope = self.PitchIntervalEnvelope(envelope_or_envelope_argument)
        self._envelope = envelope

    # ###################################################################### #
    #                            comparison methods                          #
    # ###################################################################### #

    @abc.abstractmethod
    def add(self, pitch_interval: PitchInterval, mutate: bool = True) -> Pitch:
        raise NotImplementedError

    @abc.abstractmethod
    def subtract(self, pitch_interval: PitchInterval, mutate: bool = True) -> Pitch:
        raise NotImplementedError

    def __add__(self, pitch_interval: PitchInterval) -> Pitch:
        return self.add(pitch_interval, mutate=False)

    def __sub__(self, pitch_interval: PitchInterval) -> Pitch:
        return self.subtract(pitch_interval, mutate=False)

    def resolve_envelope(
        self,
        duration: core_constants.DurationType,
        resolve_envelope_class: typing.Optional[type[core_events.Envelope]] = None,
    ) -> core_events.Envelope:
        if not resolve_envelope_class:
            resolve_envelope_class = Pitch.PitchEnvelope
        return super().resolve_envelope(duration, resolve_envelope_class)

    def get_pitch_interval(self, pitch_to_compare: Pitch) -> PitchInterval:
        """Get :class:`PitchInterval` between itself and other pitch

        :param pitch_to_compare: The pitch which shall be compared to
            the active pitch.
        :type pitch_to_compare: Pitch
        :return: :class:`PitchInterval` between

        **Example:**

        >>> from mutwo import music_parameters
        >>> a4 = music_parameters.DirectPitch(frequency=440)
        >>> a5 = music_parameters.DirectPitch(frequency=880)
        >>> a4.get_pitch_interval(a5)
        DirectPitchInterval(cents = 1200)
        """

        cent_difference = self.ratio_to_cents(
            pitch_to_compare.frequency / self.frequency
        )
        return music_parameters.DirectPitchInterval(cent_difference)


@functools.total_ordering  # type: ignore
class Volume(
    core_parameters.abc.SingleNumberParameter,
    value_name="amplitude",
    value_return_type=float,
):
    """Abstract base class for any volume class.

    If the user wants to define a new volume class, the abstract
    property :attr:`amplitude` has to be overridden.
    """

    @staticmethod
    def decibel_to_amplitude_ratio(
        decibel: core_constants.Real, reference_amplitude: core_constants.Real = 1
    ) -> float:
        """Convert decibel to amplitude ratio.

        :param decibel: The decibel number that shall be converted.
        :param reference_amplitude: The amplitude for decibel == 0.

        **Example:**

        >>> from mutwo.parameters import abc
        >>> abc.Volume.decibel_to_amplitude_ratio(0)
        1
        >>> abc.Volume.decibel_to_amplitude_ratio(-6)
        0.5011872336272722
        >>> abc.Volume.decibel_to_amplitude_ratio(0, reference_amplitude=0.25)
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

        >>> from mutwo.parameters import abc
        >>> abc.Volume.decibel_to_power_ratio(0)
        1
        >>> abc.Volume.decibel_to_power_ratio(-6)
        0.251188643150958
        >>> abc.Volume.decibel_to_power_ratio(0, reference_amplitude=0.25)
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

        >>> from mutwo.parameters import abc
        >>> abc.Volume.amplitude_ratio_to_decibel(1)
        0
        >>> abc.Volume.amplitude_ratio_to_decibel(0)
        inf
        >>> abc.Volume.amplitude_ratio_to_decibel(0.5)
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

        >>> from mutwo.parameters import abc
        >>> abc.Volume.power_ratio_to_decibel(1)
        0
        >>> abc.Volume.power_ratio_to_decibel(0)
        inf
        >>> abc.Volume.power_ratio_to_decibel(0.5)
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

        >>> from mutwo.parameters import abc
        >>> abc.Volume.amplitude_ratio_to_midi_velocity(1)
        127
        >>> abc.Volume.amplitude_ratio_to_midi_velocity(0)
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

        >>> from mutwo.parameters import abc
        >>> abc.Volume.decibel_to_midi_velocity(0)
        127
        >>> abc.Volume.decibel_to_midi_velocity(-40)
        0
        """

        if minimum_decibel is None:
            minimum_decibel = (
                music_parameters.configurations.DEFAULT_MINIMUM_DECIBEL_FOR_MIDI_VELOCITY_AND_STANDARD_DYNAMIC_INDICATOR
            )

        if maximum_decibel is None:
            maximum_decibel = (
                music_parameters.configurations.DEFAULT_MAXIMUM_DECIBEL_FOR_MIDI_VELOCITY_AND_STANDARD_DYNAMIC_INDICATOR
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

    # properties
    @property
    def decibel(self) -> core_constants.Real:
        """The decibel of the volume (from -120 to 0)"""
        return self.amplitude_ratio_to_decibel(self.amplitude)

    @property
    def midi_velocity(self) -> int:
        """The velocity of the volume (from 0 to 127)."""
        return self.decibel_to_midi_velocity(self.decibel)


class PitchAmbitus(abc.ABC):
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
    def pitch_to_period(self, pitch: Pitch) -> PitchInterval:
        raise NotImplementedError

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
            objects method :method:`pitch_to_period`. Default to `None`.
        :type period: typing.Optional[PitchInterval]
        """

        if period is None:
            period = self.pitch_to_period(pitch)

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
                music_parameters.JustIntonationPitch('1/2'),
                music_parameters.JustIntonationPitch('2/1'),
            )
        >>> ambitus0.filter_pitch_sequence(
                [
                    music_parameters.JustIntonationPitch("3/8"),
                    music_parameters.JustIntonationPitch("3/4"),
                    music_parameters.JustIntonationPitch("3/2"),
                    music_parameters.JustIntonationPitch("3/1"),
                ]
            )
        (JustIntonationPitch('3/4'), JustIntonationPitch('3/2'))
        """

        return tuple(
            filter(
                lambda pitch: pitch >= self.minima_pitch and pitch <= self.maxima_pitch,
                pitch_to_filter_sequence,
            )
        )


@dataclasses.dataclass()  # type: ignore
class Indicator(abc.ABC):
    @property
    @abc.abstractmethod
    def is_active(self) -> bool:
        raise NotImplementedError()

    def get_arguments_dict(self) -> dict[str, typing.Any]:
        return {
            key: getattr(self, key)
            for key in self.__dataclass_fields__.keys()  # type: ignore
        }


class PlayingIndicator(Indicator):
    """Abstract base class for any playing indicator."""

    pass


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


@dataclasses.dataclass
class IndicatorCollection(typing.Generic[T]):
    def get_all_indicator(self) -> tuple[T, ...]:
        return tuple(
            getattr(self, key)
            for key in self.__dataclass_fields__.keys()  # type: ignore
        )

    def get_indicator_dict(self) -> dict[str, Indicator]:
        return {key: getattr(self, key) for key in self.__dataclass_fields__.keys()}  # type: ignore


class Lyric(
    core_parameters.abc.SingleValueParameter,
    value_name="phonetic_representation",
    value_return_type=str,
):
    """Abstract base class for any spoken, sung or written text.

    If the user wants to define a new lyric class, the abstract
    properties :attr:`phonetic_representation` and
    :attr:`written_representation` have to be overridden.

    The :attr:`phonetic_representation` should return a string of
    X-SAMPA format phonemes, separated by space to indicate new words.
    Consult `wikipedia entry <https://en.wikipedia.org/wiki/X-SAMPA>`_
    for detailed information regarding X-SAMPA.

    The :attr:`written_representation` should return a string of
    normal written text, separated by space to indicate new words.
    """

    @property
    def written_representation(self) -> str:
        """Get text as it would be written in natural language"""
        raise NotImplementedError


class Syllable(Lyric):
    """Syllable mixin for classes which inherit from :class:`Lyric`.

    This adds the new attribute :attr:`is_last_syllable`. This should
    be `True` if it is the last syllable of a word and `False` if it
    isn't.
    """

    def __init__(self, is_last_syllable: bool):
        self.is_last_syllable = is_last_syllable
