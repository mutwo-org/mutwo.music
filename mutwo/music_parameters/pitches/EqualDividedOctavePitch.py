from __future__ import annotations

import operator
import typing


from mutwo import core_constants
from mutwo import core_utilities
from mutwo import music_parameters


__all__ = ("EqualDividedOctavePitch",)

ConcertPitch = core_constants.Real | music_parameters.abc.Pitch


class EqualDividedOctavePitch(music_parameters.abc.Pitch):
    """Pitch that is tuned to an Equal divided octave tuning system.

    :param pitch_class_count: how many pitch classes in each octave
        occur (for instance 12 for a chromatic system, 24 for quartertones, etc.)
    :param pitch_class: The pitch class of the new :class:`EqualDividedOctavePitch` object.
    :param octave: The octave of the new :class:`EqualDividedOctavePitch` object (where 0 is
        the middle octave, 1 is one octave higher and -1 is one octave lower).
    :param concert_pitch_pitch_class: The pitch class of the reference pitch (for
        instance 9 in a chromatic 12 tone system where `a` should be the reference
        pitch).
    :param concert_pitch_octave: The octave of the reference pitch.
    :param concert_pitch: The frequency of the reference pitch (for instance 440 for a).

    >>> from mutwo import music_parameters
    >>> # making a middle `a`
    >>> pitch = music_parameters.EqualDividedOctavePitch(12, 9, 4, 9, 4, 440)
    """

    def __init__(
        self,
        pitch_class_count: int,
        pitch_class: core_constants.Real,
        octave: int,
        concert_pitch_pitch_class: core_constants.Real,
        concert_pitch_octave: int,
        concert_pitch: ConcertPitch = None,
        *args,
        **kwargs,
    ):
        super().__init__(
            *args,
            **kwargs,
        )
        concert_pitch = (
            concert_pitch or music_parameters.configurations.DEFAULT_CONCERT_PITCH
        )

        self._pitch_class_count = pitch_class_count
        self.pitch_class = pitch_class
        self.octave = octave
        self.concert_pitch_pitch_class = concert_pitch_pitch_class
        self.concert_pitch_octave = concert_pitch_octave
        self.concert_pitch = concert_pitch  # type: ignore

    # ###################################################################### #
    #                          private methods                               #
    # ###################################################################### #

    def _assert_correct_pitch_class(self, pitch_class: core_constants.Real) -> None:
        """Makes sure the respective pitch_class is within the allowed range."""

        try:
            assert all((pitch_class <= self.pitch_class_count - 1, pitch_class >= 0))
        except AssertionError:
            raise ValueError(
                f"Invalid pitch class {pitch_class}!. "
                "Pitch_class has to be in range (min = 0, max"
                f" = {self.pitch_class_count - 1})."
            )

    def _math(
        self,
        pitch_class_delta: core_constants.Real,
        operator: typing.Callable[
            [core_constants.Real, core_constants.Real], core_constants.Real
        ],
    ) -> None:
        # Round to avoid floating point errors
        new_pitch_class = core_utilities.round_floats(
            operator(self.pitch_class, pitch_class_delta), 10
        )
        octave_delta = new_pitch_class // self.pitch_class_count
        new_pitch_class = new_pitch_class % self.pitch_class_count
        new_octave = self.octave + octave_delta
        self.pitch_class = new_pitch_class
        self.octave = int(new_octave)

    # ###################################################################### #
    #                          public properties                             #
    # ###################################################################### #

    @property
    def pitch_class_count(self) -> int:
        """Defines in how many different pitch classes one octave get divided."""
        return self._pitch_class_count

    @property
    def concert_pitch(self) -> music_parameters.abc.Pitch:
        """The referential concert pitch for the respective pitch object."""
        return self._concert_pitch

    @concert_pitch.setter
    def concert_pitch(self, concert_pitch: ConcertPitch) -> None:
        if not isinstance(concert_pitch, music_parameters.abc.Pitch):
            concert_pitch = music_parameters.DirectPitch(concert_pitch)

        self._concert_pitch = concert_pitch

    @property
    def concert_pitch_pitch_class(self) -> core_constants.Real:
        """The pitch class of the referential concert pitch."""
        return self._concert_pitch_pitch_class

    @concert_pitch_pitch_class.setter
    def concert_pitch_pitch_class(self, pitch_class: core_constants.Real) -> None:
        self._assert_correct_pitch_class(pitch_class)
        self._concert_pitch_pitch_class = pitch_class

    @property
    def pitch_class(self) -> core_constants.Real:
        """The pitch class of the pitch."""
        return self._pitch_class

    @pitch_class.setter
    def pitch_class(self, pitch_class: core_constants.Real) -> None:
        self._assert_correct_pitch_class(pitch_class)
        self._pitch_class = pitch_class

    @property
    def step_factor(self):
        """The factor with which to multiply a frequency to reach the next pitch."""
        return pow(2, 1 / self.pitch_class_count)

    @property
    def step_size(self) -> float:
        """This property describes how many cents are between two adjacent pitches."""
        return self.ratio_to_cents(self.step_factor)

    @property
    def hertz(self) -> float:
        octave_delta = self.octave - self.concert_pitch_octave
        pitch_class_delta = self.pitch_class - self.concert_pitch_pitch_class
        cents = (octave_delta * music_parameters.constants.OCTAVE_IN_CENTS) + (
            self.step_size * pitch_class_delta
        )
        ratio = self.cents_to_ratio(cents)
        return core_utilities.round_floats(
            self.concert_pitch.hertz * ratio,
            music_parameters.configurations.EQUAL_DIVIDED_OCTAVE_PITCH_ROUND_FREQUENCY_DIGIT_COUNT,
        )

    # ###################################################################### #
    #                          public methods                                #
    # ###################################################################### #

    def add(
        self, pitch_interval: music_parameters.abc.PitchInterval.Type
    ) -> EqualDividedOctavePitch:
        self._math(
            music_parameters.abc.PitchInterval.from_any(pitch_interval).cents
            / self.step_size,
            operator.add,
        )
        return self

    def add_pitch_class_delta(
        self, pitch_class_delta: core_constants.Real
    ) -> EqualDividedOctavePitch:
        self._math(pitch_class_delta, operator.add)
        return self

    def subtract_pitch_class_delta(
        self, pitch_class_delta: core_constants.Real
    ) -> EqualDividedOctavePitch:
        return self.add_pitch_class_delta(-pitch_class_delta)
