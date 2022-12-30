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
import itertools
import math
import types
import typing
import yaml

try:
    import quicktions as fractions  # type: ignore
except ImportError:
    import fractions  # type: ignore

import numpy as np
import ranges

from mutwo import core_constants
from mutwo import core_events
from mutwo import core_parameters
from mutwo import core_utilities
from mutwo import music_parameters
from mutwo import music_utilities

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
    "BodyPart",
    "Fingering",
)


class PitchInterval(
    core_parameters.abc.SingleNumberParameter,
    value_name="interval",
    value_return_type=float,
):
    """Abstract base class for any pitch interval class

    If the user wants to define a new pitch interval class, the abstract
    property :attr:`interval` and the abstract method `inverse`
    have to be overridden.

    :attr:`interval` is stored in unit `cents`.

    See `wikipedia entry <https://en.wikipedia.org/wiki/Cent_(music)>`_
    for definition of 'cents'.
    """

    def __repr__(self) -> str:
        return str(self)

    @abc.abstractmethod
    def inverse(self, mutate: bool = False) -> PitchInterval:
        """Makes falling interval to rising and vice versa.

        In `music21` the method for equal semantics is called
        `reverse <https://web.mit.edu/music21/doc/moduleReference/moduleInterval.html#music21.interval.Interval.reverse >`_.
        """

    def __add__(self, other: PitchInterval) -> PitchInterval:
        return music_parameters.DirectPitchInterval(self.interval + other.interval)

    def __sub__(self, other: PitchInterval) -> PitchInterval:
        return music_parameters.DirectPitchInterval(self.interval - other.interval)


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
    to define an :func:`add` method.
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
            event_to_parameter = event_to_parameter or self._event_to_parameter
            value_to_parameter = value_to_parameter or self._value_to_parameter
            apply_parameter_on_event = (
                apply_parameter_on_event or self._apply_parameter_on_event
            )
            parameter_to_value = parameter_to_value or self._parameter_to_value

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
                Pitch.PitchIntervalEnvelope | typing.Sequence
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
        envelope: typing.Optional[Pitch.PitchIntervalEnvelope | typing.Sequence] = None,
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
            Pitch.PitchIntervalEnvelope | typing.Sequence
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
        ...

    @core_utilities.add_copy_option
    def subtract(self, pitch_interval: music_parameters.abc.PitchInterval) -> Pitch:
        return self.add(music_parameters.DirectPitchInterval(-pitch_interval.interval))  # type: ignore

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
        >>> pitch_interval = a4.get_pitch_interval(a5)
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
        ...

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
            objects method :method:`pitch_to_period`. Default to `None`.
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
class Indicator(abc.ABC):
    @property
    @abc.abstractmethod
    def is_active(self) -> bool:
        ...

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


class Syllable(Lyric):
    """Syllable mixin for classes which inherit from :class:`Lyric`.

    This adds the new attribute :attr:`is_last_syllable`. This should
    be `True` if it is the last syllable of a word and `False` if it
    isn't.
    """

    def __init__(self, is_last_syllable: bool):
        self.is_last_syllable = is_last_syllable


class BodyPart(types.SimpleNamespace):
    """:class:`BodyPart` represents a part of a human body.

    :mod:`mutwo` offers `mutwo.music_parameters.constants.BODY`
    which is a default :class:`BodyPart`.

    It's recommended to use ``from_anatomy`` to initialize
    objects.
    """

    def __init__(self, name: str, **kwargs):
        self._name = name
        super().__init__(**kwargs)

    @classmethod
    def from_anatomy(cls, name: str, reference: str, anatomy: str | list) -> BodyPart:
        """Create new body part from anatomy.

        **Example:**

        >>> from mutwo import music_parameters
        >>> anatomy = r'''
        ... - id_list:
        ...     - Head
        ...   name: head
        ...   item_list:
        ...     - id_list:
        ...         - Left
        ...         - Right
        ...       name: side
        ...       item_list:
        ...         - id_list:
        ...             - Ear
        ...           name: part
        ...           item_list:
        ... '''
        >>> Body = music_parameters.abc.BodyPart.from_anatomy(
        ...     "Body", "body", anatomy
        ... )
        >>> Body.Head
        Head(body, Left, Right)
        >>> Body.Head.Left.Ear
        Ear(body, head, side)
        >>> Body.Head.Left.body == Body
        True
        """
        match anatomy:
            case str():
                anatomy = yaml.safe_load(anatomy)

        body_part = cls(name=name)

        # Recursive helper
        def _(body_part: BodyPart, anatomy: list, **kwargs):
            for item_definition in anatomy or []:
                match item_definition:
                    # Branch
                    case dict():
                        id_list, name, item_list = (
                            item_definition["id_list"],
                            item_definition["name"],
                            item_definition["item_list"],
                        )
                        for id_ in id_list:
                            new_body_part = BodyPart(id_, **kwargs)
                            setattr(body_part, id_, new_body_part)
                            _(
                                new_body_part,
                                item_list,
                                **dict(kwargs, **{name: new_body_part}),
                            )
                    # Leaf
                    case str():
                        new_body_part = BodyPart(item_definition, **kwargs)
                        setattr(body_part, item_definition, new_body_part)
                    case _:
                        raise NotImplementedError(item_definition)

        _(body_part, anatomy, **{reference: body_part})

        return body_part

    def __hash__(self) -> int:
        return id(self)

    # Filtered __dict__
    @property
    def _item_dict(self) -> dict:
        return {
            key: value
            for key, value in self.__dict__.items()
            if key not in ("_name", "name")
        }

    def __repr__(self) -> str:
        items = ", ".join(self._item_dict.keys())
        return f"{self.name}({items})"

    def __str__(self) -> str:
        return self.__repr__()

    @property
    def name(self) -> str:
        return self._name


# Declare BODY constant here to avoid circular import
# error.
music_parameters.constants.BODY = BodyPart.from_anatomy(
    "Body",
    "body",
    music_parameters.constants.ANATOMY,
)

T = typing.TypeVar("T", bound=core_events.abc.Event)


# Use _frozenset for all fingering related sets, to avoid
# overriding repr multiple times.
class _frozenset(frozenset, typing.Generic[T]):
    def __repr__(self) -> str:
        return f"{type(self).__name__}({str(set(self))})"


class Fingering(_frozenset, metaclass=abc.ABCMeta):
    """Map body parts to positions in physical space.

    :param fingering_part_iterable: A fingering is composed of
        body part to vector mappings. Each mapping is described
        by :class:`Fingering.Part` objects.
    :type fingering_part_iterable: typing.Iterable[Fingering.Part]

    With :class:`Fingering`s it's possible to describe how a certain
    sound can be played on a specific instrument. By being able
    to describe this, we can model how difficult or easy it is to
    play a specific sequence of sounds on a given instrument.

    :class:`Fingering` describes how the sound can be produced by
    mapping human body parts to positions in a physical space.

    Body parts are represented by :class:`BodyPart` instances.
    Positions in a physical space are represented by
    vectors (:class:`collections.namedtuple`). Each instrument
    fingering uses a predefined tuple size where each element
    represents a specific property of a physical space.

    For instance the vector of a Spanish guitar is composed of

        ``(string_index, fret_index)``

    so that

        ``(1, 2)``

    specifies the second fret on the 'A' - string.

    :class:`Fingering` functions as a namespace for related
    objects:

    - Instances of :class:`Fingering.Vector` model a
      certain position in physical space.

    - Instances of :class:`Fingering.Part` model partial
      aspects of a fingering.

    - Instances of :class:`Fingering.Delta` model differences
      between two :class:`Fingering` instances.

    - Instances of :class:`Fingering.Part.Delta` model
      differences between two :class:`Fingering.Part`
      instances.

    - Instances of :class:`Fingering.DeltaSet` model
      differences between a given fingering and all its
      predecessors and successors.

    In order to inherit from :class:`Fingering` class the
    user needs to override the abstract class property
    ``Vector`` of :class:`Fingering` and the abstract property
    ``score`` of :class:`Fingering.Part.Delta`.

    **Example:**

    >>> import collections
    >>> from mutwo import music_parameters
    >>> # We model a very simple Xylophone with only two bars.
    >>> body = music_parameters.constants.BODY
    >>> class MyInstrument(music_parameters.DiscreetPitchedInstrument):
    ...     def __init__(self):
    ...         super().__init__(
    ...             (
    ...                 music_parameters.WesternPitch('c'),
    ...                 music_parameters.WesternPitch('a')
    ...             ),
    ...             'xylophone'
    ...         )
    ...     class Fingering(music_parameters.abc.Fingering):
    ...         class Vector(collections.namedtuple('Vector', ('bar',))):
    ...             def __sub__(self, other): return type(self)(self.bar - other.bar)
    ...         class Part(music_parameters.abc.Fingering.Part):
    ...             class Delta(music_parameters.abc.Fingering.Part.Delta):
    ...                 # Extremely simplified score method which
    ...                 # ignores body parts.
    ...                 @property
    ...                 def score(self) -> float:
    ...                     return sum((1 if vector.bar == 0 else 0.5 for vector in self.vector_set))
    ...     def pitch_tuple_to_fingering_tuple(self, pitch_tuple):
    ...         pitch = pitch_tuple[0]
    ...         if pitch == music_parameters.WesternPitch('c'):
    ...             bar_index = 0
    ...         elif pitch == music_parameters.WesternPitch('a'):
    ...             bar_index = 1
    ...         else:
    ...             raise NotImplementedError(pitch)
    ...         return self.Fingering(
    ...             {
    ...                 self.Fingering.Part(
    ...                     body.Left.Arm.Hand.Finger.One,
    ...                     frozenset((self.Fingering.Vector(bar_index),))
    ...                 )
    ...             }
    ...         ),
    >>> instr = MyInstrument()
    >>> fingering0, *_ = instr.pitch_tuple_to_fingering_tuple(
    ...     (music_parameters.WesternPitch('c'),)
    ... )
    >>> fingering1, *_ = instr.pitch_tuple_to_fingering_tuple(
    ...     (music_parameters.WesternPitch('a'),)
    ... )
    >>> delta = fingering0.delta(fingering1)
    >>> print(delta)
    Delta({MyInstrument.Fingering.Part.Delta(body_part_start=One(body, side, limb, appendage, digit), body_part_end=One(body, side, limb, appendage, digit), vector_set=frozenset({Vector(bar=1)}))})
    >>> delta.score
    0.5
    >>> fingering0.delta(fingering0).score
    1.0
    """

    # This should be a classmethod + a property. Abstractmethod
    # is ineffective in inherited classes if we add classmethod and
    # property decorators.
    #
    # @classmethod
    # @property
    @abc.abstractmethod
    def Vector(cls):
        """Returns  ``Vector`` class to represent position in physical space.

        This is usually a ``collections.namedtuple`` instance.
        """

    @dataclasses.dataclass(frozen=True)
    class Part(object):
        """Map a :class:`BodyPart` to a position in the physical space.

        :param body_part: Tells which part of a human body touches the
            specific position in a physical space.
        :type body_part: BodyPart
        :param vector_set: Tells which position in a physical space
            is touched by parts of a human body.
        :type vector_set: frozenset[Fingering.Vector]
        :param sound: Assigns which sound is produced by the given
            :class:`Fingering.Part`. This could be a ``tuple`` of
            :class:`Pitch`es, for instance. Default to ``None``.
        :type sound: typing.Any
        """

        body_part: BodyPart
        vector_set: frozenset[Fingering.Vector]
        sound: typing.Any = None

        @dataclasses.dataclass(frozen=True, unsafe_hash=True)
        class Delta(abc.ABC):
            """:class:`Fingering.Part.Delta` represents the difference between two :class:`Fingering.Part`s.

            :param body_part_start: The previously active :class:`BodyPart`..
            :type body_part_start: BodyPart
            :param body_part_end: The currently active :class:`BodyPart`.
            :type body_part_end: BodyPart
            :param vector_set: Collects the difference between the old vectors
                and current vectors.
            :type vector_set: frozenset[Fingering.Vector]
            """

            body_part_start: BodyPart
            body_part_end: BodyPart
            vector_set: frozenset[Fingering.Vector]

            @property
            @abc.abstractmethod
            def score(self) -> float:
                """Fetch playability of a :class:`Fingering.Delta`.

                A high return value indicates that the fingering change
                is easily playable.

                The ``score`` depends on both body parts and the Δ vector.
                """

        def __hash__(self) -> int:
            return hash((self.body_part, self.vector_set))

        def delta(self, other: Fingering.Part) -> Fingering.Part.Delta:
            """Calculate Δ between two :class:`Fingering.Part`s.

            :param other: The other fingering to calculate the delta.
            :type other: Fingering
            :param distance: How far the other finger is from the
                current delta. Default to 1.
            :type distance: int
            """
            return self.Delta(
                body_part_start=self.body_part,
                body_part_end=other.body_part,
                vector_set=frozenset(
                    [
                        v1 - v0
                        for v0, v1 in itertools.product(
                            self.vector_set, other.vector_set
                        )
                    ]
                ),
            )

    class Delta(_frozenset[Part.Delta, ...]):
        """:class:`Fingering.Delta` represents the difference between two fingerings.

        :param part_delta_iterable: The delta between fingerings is
            represented by the delta between :class:`Fingering.Part`s.
        :type part_delta_iterable: typing.Iterable[Fingering.Part.Delta]
        :param distance: Indicates how far away (long ago) the previous
            or next :class:`Fingering` is. Distance matters for the
            calculation of :class:`Fingering.DeltaSet`s ``score`` property,
            but doesn't matter for the calculation of
            :class:`Fingering.Delta`s ``score`` property. A higher
            ``distance`` results in a smaller importance (weight) of the
            given :class:``Fingering.Delta`` in the summed up
            ``score``.
        :type distance: int
        """

        def __new__(
            self,
            part_delta_iterable: typing.Iterable[Fingering.Part.Delta],
            distance: int = 1,
        ):
            if not distance:
                raise music_utilities.IllegalFingeringDistanceError(distance)
            delta = super().__new__(self, part_delta_iterable)
            delta._distance = distance
            return delta

        @property
        def distance(self) -> int:
            """Sets how far away the previous/next :class:`Fingering` is."""
            return self._distance

        @functools.cached_property
        def score(self) -> float:
            """Fetch playability of a :class:`Fingering.Delta`.

            A high return value indicates that the fingering change
            is easily playable.
            """
            if score_list := [d.score for d in self]:
                return float(np.average(score_list))
            return 1  # No relevant delta found => can be played

    class DeltaSet(_frozenset[Delta, ...]):
        """:class:`Fingering.DeltaSet` collects :class:`Fingering.Delta`.

        :param delta_iterable: All differences between relevant predecessors
            and successors of a :class:`Fingering`.
        :type delta_iterable: typing.Iterable[Fingering.Delta]

        :class:`DeltaSet` helps calculating the ``score`` of multiple
        ``Delta`` (e.g. differences not only to the last fingering but
        also to fingerings before a given fingering).
        """

        @functools.cached_property
        def score(self) -> float:
            """Fetch playability of a :class:`Fingering.DeltaSet`.

            A high return value indicates that the fingering change
            is easily playable.
            """
            return float(np.average((d.score for d in self)))

    def delta(self, other: Fingering, distance: int = 1) -> Fingering.Delta:
        """Calculate Δ between two fingerings.

        :param other: The other fingering to calculate the delta.
        :type other: Fingering
        :param distance: How far the other finger is from the current delta.
        :type distance: int
        """
        delta_list = []  # We collect delta between parts.
        for p0, p1 in itertools.product(self, other):
            delta_list.append(p0.delta(p1))
        return self.Delta(delta_list, distance=distance)


@dataclasses.dataclass(frozen=True)
class Instrument(abc.ABC):
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
    def __contains__(self, pitch: typing.Any) -> bool:
        ...

    @property
    @abc.abstractmethod
    def pitch_ambitus(self) -> music_parameters.abc.PitchAmbitus:
        ...

    @property
    def is_pitched(self) -> bool:
        return True

    # We need to parse a `pitch_sequence` and not only a single
    # pitch, because a certain combination of pitches needs a different
    # fingering then only one single pitch (we can't combine fingering
    # parts afterwards).
    # We need to return a tuple of fingerings and not only one fingering,
    # because we want to fetch all possible fingerings and not only one
    # option. If we don't have any options at all, we can therefore also
    # simply return an empty tuple.
    def pitch_sequence_to_fingering_tuple(
        self, pitch_sequence: typing.Sequence[Pitch]
    ) -> tuple[Fingering, ...]:
        """Find all possible :class:`Fingering`s to play harmony on instrument.

        :param pitch_sequence: The chord to be played by the
            instrument.
        :type pitch_sequence: typing.Sequence[Pitch]
        """
        return tuple([])

    @abc.abstractmethod
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

        This is not necessarily the same as
        ``instrument.pitch_ambitus.get_pitch_variant_tuple()``, because
        a :class:`mutwo.music_parameters.DiscreetPitchedInstrument` may
        not be capable of playing a pitch even if the given pitch is within
        the ambitus of an instrument. It's therefore recommended to
        use ``instrument.get_pitch_variant_tuple`` if one wants to find
        out in which octaves the given pitch is actually playable on the
        instrument.
        """
