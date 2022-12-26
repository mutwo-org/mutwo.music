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

    :param n_pitch_classes_per_octave: how many pitch classes in each octave
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
        n_pitch_classes_per_octave: int,
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

        self._n_pitch_classes_per_octave = n_pitch_classes_per_octave
        self.pitch_class = pitch_class
        self.octave = octave
        self.concert_pitch_pitch_class = concert_pitch_pitch_class
        self.concert_pitch_octave = concert_pitch_octave
        self.concert_pitch = concert_pitch  # type: ignore

    # ###################################################################### #
    #                          magic methods                                 #
    # ###################################################################### #

    def __sub__(self, other: EqualDividedOctavePitch) -> core_constants.Real:
        """Calculates the interval between two ``EqualDividedOctave`` pitches."""

        try:
            assert self.n_pitch_classes_per_octave == other.n_pitch_classes_per_octave
        except AssertionError:
            raise ValueError(
                "Can't calculate the interval between to different"
                " EqualDividedOctavePitch objects with different value for"
                " 'n_pitch_classes_per_octave'."
            )

        n_pitch_classes_difference = self.pitch_class - other.pitch_class
        n_octaves_difference = self.octave - other.octave
        return n_pitch_classes_difference + (
            n_octaves_difference * self.n_pitch_classes_per_octave
        )

    # ###################################################################### #
    #                          private methods                               #
    # ###################################################################### #

    def _assert_correct_pitch_class(self, pitch_class: core_constants.Real) -> None:
        """Makes sure the respective pitch_class is within the allowed range."""

        try:
            assert all(
                (pitch_class <= self.n_pitch_classes_per_octave - 1, pitch_class >= 0)
            )
        except AssertionError:
            raise ValueError(
                f"Invalid pitch class {pitch_class}!. "
                "Pitch_class has to be in range (min = 0, max"
                f" = {self.n_pitch_classes_per_octave - 1})."
            )

    def _fetch_n_pitch_classes_difference(
        self,
        pitch_interval: music_parameters.abc.PitchInterval | core_constants.Real,
    ) -> core_constants.Real:
        if isinstance(
            pitch_interval,
            music_parameters.abc.PitchInterval,
        ):
            return pitch_interval.interval / self.n_cents_per_step
        else:
            return pitch_interval

    def _math(
        self,
        n_pitch_classes_difference: core_constants.Real,
        operator: typing.Callable[
            [core_constants.Real, core_constants.Real], core_constants.Real
        ],
    ) -> None:
        new_pitch_class = operator(self.pitch_class, n_pitch_classes_difference)
        n_octaves_difference = new_pitch_class // self.n_pitch_classes_per_octave
        new_pitch_class = new_pitch_class % self.n_pitch_classes_per_octave
        new_octave = self.octave + n_octaves_difference
        self.pitch_class = new_pitch_class
        self.octave = int(new_octave)

    # ###################################################################### #
    #                          public properties                             #
    # ###################################################################### #

    @property
    def n_pitch_classes_per_octave(self) -> int:
        """Defines in how many different pitch classes one octave get divided."""
        return self._n_pitch_classes_per_octave

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
        return pow(2, 1 / self.n_pitch_classes_per_octave)

    @property
    def n_cents_per_step(self) -> float:
        """This property describes how many cents are between two adjacent pitches."""
        return self.ratio_to_cents(self.step_factor)

    @property
    def frequency(self) -> float:
        n_octaves_distant_to_concert_pitch = self.octave - self.concert_pitch_octave
        n_pitch_classes_distant_to_concert_pitch = (
            self.pitch_class - self.concert_pitch_pitch_class
        )
        distance_to_concert_pitch_in_cents = (
            n_octaves_distant_to_concert_pitch
            * music_parameters.constants.OCTAVE_IN_CENTS
        ) + (self.n_cents_per_step * n_pitch_classes_distant_to_concert_pitch)
        distance_to_concert_pitch_as_factor = self.cents_to_ratio(
            distance_to_concert_pitch_in_cents
        )
        return core_utilities.round_floats(
            self.concert_pitch.frequency * distance_to_concert_pitch_as_factor,
            music_parameters.configurations.EQUAL_DIVIDED_OCTAVE_PITCH_ROUND_FREQUENCY_DIGIT_COUNT,
        )

    # ###################################################################### #
    #                          public methods                                #
    # ###################################################################### #

    @core_utilities.add_copy_option
    def add(  # type: ignore
        self, pitch_interval: music_parameters.abc.PitchInterval | core_constants.Real
    ) -> EqualDividedOctavePitch:  # type: ignore
        """Transposes the ``EqualDividedOctavePitch`` by n_pitch_classes_difference."""

        n_pitch_classes_difference = self._fetch_n_pitch_classes_difference(
            pitch_interval
        )
        self._math(n_pitch_classes_difference, operator.add)

    @core_utilities.add_copy_option
    def subtract(  # type: ignore
        self, pitch_interval: music_parameters.abc.PitchInterval | core_constants.Real
    ) -> EqualDividedOctavePitch:  # type: ignore
        """Transposes the ``EqualDividedOctavePitch`` by n_pitch_classes_difference."""
        if isinstance(
            pitch_interval,
            music_parameters.abc.PitchInterval,
        ):
            return super().subtract(pitch_interval)  # type: ignore
        else:
            return self.add(-pitch_interval)
