from __future__ import annotations

import re
import warnings

from mutwo import core_constants
from mutwo import core_utilities
from mutwo import music_parameters

__all__ = (
    "DirectPitchInterval",
    "WesternPitchInterval",
)


class DirectPitchInterval(music_parameters.abc.PitchInterval):
    """Simple interval class which gets directly assigned by its cents value

    :param interval: Defines how big or small the interval is (in cents).
    :type interval: float

    **Example:**

    >>> from mutwo import music_parameters
    >>> rising_octave = music_parameters.DirectPitchInterval(1200)
    >>> falling_minor_third = music_parameters.DirectPitchInterval(-300)
    """

    def __init__(self, interval: float):
        self.interval = interval

    @property
    def interval(self) -> float:
        return self._interval

    @interval.setter
    def interval(self, interval: float):
        self._interval = interval

    @core_utilities.add_copy_option
    def inverse(self, mutate: bool = False) -> DirectPitchInterval:
        """Makes falling interval to rising and vice versa.

        **Example:**

        >>> from mutwo import music_parameters
        >>> music_parameters.DirectPitchInterval(700).inverse().interval
        -700
        """
        self.interval = -self.interval
        return self


class WesternPitchInterval(music_parameters.abc.PitchInterval):
    """Model intervals by using European music theory based representations

    :param interval_name_or_semitone_count: Can be either an interval name
        (a string) or a number for semitones. When using an interval
        name is should have the form: QUALITY-IS_FALLING-TYPE, e.g. for having
        a rising perfect fourth (where 'fourth' is the type and 'perfect' the
        quality) you can write "p4". For a falling perfect fourth it would
        be "p-4". The interval names are equal to the specification used
        in the python library `music21 <http://web.mit.edu/music21/>`_.
        Please also consult the specification of the quality abbreviations at
        :const:`mutwo.music_parameters.configurations.WESTERN_PITCH_INTERVAL_QUALITY_NAME_TO_ABBREVIATION_DICT`
        and the specification of the `is-interval-falling` indicator
        :const:`mutwo.music_parameters.configurations.FALLING_WESTERN_PITCH_INTERVAL_INDICATOR`.
        Both can be changed by the user. Default to 'p1'.
    :type interval_name_or_semitone_count: str | core_constants.Real

    This class is particularly useful in combination with
    :class:`mutwo.music_parameters.WesternPitch`.

    **Disclaimer:**

    Although :class:`mutwo.music_parameters.WesternPitch` does support
    microtones, :class:`WesternPitchInterval` does not.

    **Example:**

    >>> from mutwo import music_parameters
    >>> perfect_fifth = music_parameters.WesternPitchInterval('p5')
    >>> falling_major_third = music_parameters.WesternPitchInterval('M-3')
    >>> minor_third = music_parameters.WesternPitchInterval('m3')
    >>> falling_octave = music_parameters.WesternPitchInterval(-12)
    >>> augmented_octave = music_parameters.WesternPitchInterval('A8')
    >>> very_diminished_sixth = music_parameters.WesternPitchInterval('dddd6')
    """

    def __init__(
        self,
        interval_name_or_semitone_count: str | core_constants.Real = "p1",
    ):
        # Define mapping on the fly, so that it is only necessary to adjust
        # music_parameters.configurations.WESTERN_PITCH_INTERVAL_QUALITY_NAME_TO_ABBREVIATION_DICT
        # if user wants to use different abbreviations.
        self._abbreviation_to_western_pitch_interval_quality_name_dict = {
            abbreviation: western_pitch_interval_quality
            for western_pitch_interval_quality, abbreviation in music_parameters.configurations.WESTERN_PITCH_INTERVAL_QUALITY_NAME_TO_ABBREVIATION_DICT.items()
        }

        if isinstance(interval_name_or_semitone_count, str):
            to_interval_data = WesternPitchInterval._interval_name_to_interval_data
        else:
            to_interval_data = WesternPitchInterval._semitone_count_to_interval_data

        self._set_attribute_by_interval_data(
            *to_interval_data(interval_name_or_semitone_count)  # type: ignore
        )

    # ###################################################################### #
    #                      static private methods                            #
    # ###################################################################### #

    @staticmethod
    def _interval_type_to_interval_base_type(interval_type: str) -> str:
        return str(
            (
                (int(interval_type) - 1)
                % music_parameters.constants.WESTERN_PITCH_INTERVAL_BASE_TYPE_COUNT
            )
            + 1
        )

    @staticmethod
    def _interval_type_to_octave_count(interval_type: str) -> int:
        return int(
            (
                (int(interval_type) - 1)
                // music_parameters.constants.WESTERN_PITCH_INTERVAL_BASE_TYPE_COUNT
            )
        )

    @staticmethod
    def _interval_name_to_interval_data(interval_name: str) -> tuple[str, str, bool]:
        match = re.search("[0-9]+", interval_name)
        try:
            assert match is not None
        except AssertionError:
            raise Exception(
                "Found invalid interval_name '{interval_name}' "
                "without any interval type. An interval type should be"
                " an integer > 0, for instance '1' or '12' or '21'."
            )
        interval_type_start_index = interval_quality_end_index = match.span()[0]
        interval_type = interval_name[interval_type_start_index:]
        if is_interval_falling := (
            interval_name[interval_type_start_index - 1]
            == music_parameters.configurations.FALLING_WESTERN_PITCH_INTERVAL_INDICATOR
        ):
            interval_quality_end_index = interval_type_start_index - 1
        interval_quality = interval_name[:interval_quality_end_index]
        return interval_type, interval_quality, is_interval_falling

    @staticmethod
    def _semitone_count_to_interval_data(
        semitone_count: core_constants.Real,
    ) -> tuple[str, str, bool]:
        is_interval_falling = semitone_count < 0
        semitone_count = abs(semitone_count)
        semitone_count_reduced = (
            semitone_count % music_parameters.constants.CHROMATIC_PITCH_CLASS_COUNT
        )
        semitone_count_reduced_and_rounded = int(round(semitone_count_reduced))
        if semitone_count_reduced_and_rounded != semitone_count_reduced:
            warnings.warn(
                "Semitone was rounded by "
                f"'{semitone_count_reduced_and_rounded - semitone_count_reduced}'"
                " because WesternPitchInterval doesn't support microtones!",
                RuntimeWarning,
            )
        (
            interval_type,
            interval_quality,
        ) = music_parameters.constants.SEMITONE_TO_WESTERN_PITCH_INTERVAL_BASE_TYPE_AND_QUALITY_DICT[
            semitone_count_reduced_and_rounded
        ]
        interval_quality_abbreviation = music_parameters.configurations.WESTERN_PITCH_INTERVAL_QUALITY_NAME_TO_ABBREVIATION_DICT[
            interval_quality
        ]
        octave_count = int(
            semitone_count // music_parameters.constants.CHROMATIC_PITCH_CLASS_COUNT
        )
        interval_type = str(int(interval_type) + (octave_count * 7))
        return interval_type, interval_quality_abbreviation, is_interval_falling

    @staticmethod
    def _assert_interval_quality_avoids_illegal_stacking(
        interval_quality_tuple: tuple[str, ...]
    ):
        if len(interval_quality_tuple) > 1:
            try:
                assert (
                    interval_quality_tuple[0]
                    in music_parameters.constants.STACKABLE_WESTERN_PITCH_INTERVAL_QUALITY_TUPLE
                )
            except AssertionError:
                raise Exception(
                    "Found illegal stacking of interval quality "
                    f"'{interval_quality_tuple[0]}'! Only the following "
                    "interval qualities can be stacked: '"
                    f"{music_parameters.constants.STACKABLE_WESTERN_PITCH_INTERVAL_QUALITY_TUPLE}'."
                )

    @staticmethod
    def _assert_interval_quality_is_not_mixed(
        interval_quality_string: str, interval_quality_tuple: tuple[str, ...]
    ):
        try:
            assert len(set(interval_quality_tuple)) == 1
        except AssertionError:
            raise Exception(
                "Found mixed interval qualities in interval "
                f"quality string '{interval_quality_string}'. "
                "Please don't mix up interval qualities."
            )

    @staticmethod
    def _assert_interval_quality_fits_to_interval_type(
        is_perfect_interval: bool, interval_quality_tuple: tuple[str, ...]
    ):
        allowed_interval_quality_tuple = (
            music_parameters.constants.ALLOWED_WESTERN_PITCH_INTERVAL_QUALITY_FOR_IMPERFECT_INTERVAL_TUPLE,
            music_parameters.constants.ALLOWED_WESTERN_PITCH_INTERVAL_QUALITY_FOR_PERFECT_INTERVAL_TUPLE,
        )[is_perfect_interval]
        for interval_quality in interval_quality_tuple:
            try:
                assert interval_quality in allowed_interval_quality_tuple
            except AssertionError:
                raise Exception(
                    f"Found illegal interval quality '{interval_quality}' in "
                    f"interval_quality_tuple '{interval_quality_tuple}'."
                    f"For the given interval type only the "
                    "following interval qualities are allowed: "
                    f"'{allowed_interval_quality_tuple}'!"
                )

    # ###################################################################### #
    #                      static public methods                             #
    # ###################################################################### #

    @staticmethod
    def is_interval_type_perfect(interval_type: str) -> bool:
        interval_base_type = WesternPitchInterval._interval_type_to_interval_base_type(
            interval_type
        )
        return (
            interval_base_type in music_parameters.constants.PERFECT_INTERVAL_TYPE_TUPLE
        )

    @staticmethod
    def is_interval_type_imperfect(interval_type: str) -> bool:
        return not WesternPitchInterval.is_interval_type_perfect(interval_type)

    # ###################################################################### #
    #                          magic methods                                 #
    # ###################################################################### #

    def __repr__(self) -> str:
        return f"{type(self).__name__}('{self.name}')"

    def __str__(self) -> str:
        return repr(self)

    # ###################################################################### #
    #                          private methods                               #
    # ###################################################################### #

    def _set_attribute_by_interval_data(
        self, interval_type: str, interval_quality: str, is_interval_falling: bool
    ):
        self._raise_error_if_interval_quality_and_interval_type_do_not_fit(
            interval_quality, interval_type
        )
        self._raise_error_if_interval_quality_is_invalid(interval_quality)
        self._raise_error_if_interval_type_is_invalid(interval_type)

        # We can't set the interval_type and interval_quality
        # by their public property API
        # (e.g. self.interval_type = interval_type)
        # because then we would activate the tests which check if the new
        # values fit to the current object state, which could potentially
        # raise an unwanted exception.
        self._interval_type = interval_type
        self._interval_quality = interval_quality
        self.is_interval_falling = is_interval_falling

    def _raise_invalid_interval_quality_error(
        self, interval_quality_abbreviation: str, interval_quality: str
    ):
        raise NameError(
            "Found undefined interval quality abbreviation "
            f"'{interval_quality_abbreviation}'"
            f" in interval quality string '{interval_quality}'. "
            "All allowed abbreviations are only "
            f"'{self._abbreviation_to_western_pitch_interval_quality_name_dict.keys()}'."
            " Please consider overridding the keys of "
            "music_parameters.configurations.WESTERN_PITCH_INTERVAL_QUALITY_NAME_TO_ABBREVIATION_DICT"
            "if you want to use different abbreviations."
        )

    def _interval_quality_string_to_interval_quality_tuple(
        self, interval_quality_string: str
    ) -> tuple[str, ...]:
        interval_quality_list = []
        for interval_quality_abbreviation in interval_quality_string:
            try:
                interval_quality = (
                    self._abbreviation_to_western_pitch_interval_quality_name_dict[
                        interval_quality_abbreviation
                    ]
                )
            except KeyError:
                self._raise_invalid_interval_quality_error(
                    interval_quality_abbreviation, interval_quality_string
                )
            interval_quality_list.append(interval_quality)
        return tuple(interval_quality_list)

    def _raise_error_if_interval_quality_and_interval_type_do_not_fit(
        self, interval_quality: str, interval_type: str
    ):
        is_perfect_interval = WesternPitchInterval.is_interval_type_perfect(
            interval_type
        )
        interval_quality_tuple = (
            self._interval_quality_string_to_interval_quality_tuple(interval_quality)
        )
        WesternPitchInterval._assert_interval_quality_fits_to_interval_type(
            is_perfect_interval, interval_quality_tuple
        )

    def _raise_error_if_interval_quality_is_invalid(self, interval_quality: str):
        interval_quality_tuple = (
            self._interval_quality_string_to_interval_quality_tuple(interval_quality)
        )
        WesternPitchInterval._assert_interval_quality_is_not_mixed(
            interval_quality, interval_quality_tuple
        )
        WesternPitchInterval._assert_interval_quality_avoids_illegal_stacking(
            interval_quality_tuple
        )

    def _raise_error_if_interval_type_is_invalid(self, interval_type: str):
        try:
            interval_type_as_integer = int(interval_type)
        except ValueError:
            raise Exception(
                "Found invalid interval_type '{interval_type}'! "
                "An interval_type should be an integer encoded in a"
                " string e.g. '1' or '10' or '3123'."
            )
        try:
            assert interval_type_as_integer > 0
        except AssertionError:
            raise Exception(
                "Found invalid interval_type '{interval_type}'! "
                "Interval type should be bigger than 0"
            )

    # ###################################################################### #
    #                          public properties                             #
    # ###################################################################### #

    @property
    def is_interval_rising(self) -> bool:
        """Return `True` if the interval is upwards and `False` if it falls"""

        return not self.is_interval_falling

    @is_interval_rising.setter
    def is_interval_rising(self, is_interval_rising: bool):
        self.is_interval_falling = not is_interval_rising

    @property
    def interval_quality_tuple(self) -> tuple[str, ...]:
        """Parsed the interval_quality abbreviation to their full names."""

        return self._interval_quality_string_to_interval_quality_tuple(
            self.interval_quality
        )

    @property
    def interval_type(self) -> str:
        """The base interval type (e.g. octave, prime, second, ...)."""

        return self._interval_type

    @interval_type.setter
    def interval_type(self, interval_type: str):
        # Test if interval_type string is allowed
        self._raise_error_if_interval_type_is_invalid(interval_type)
        self._raise_error_if_interval_quality_and_interval_type_do_not_fit(
            self.interval_quality, interval_type
        )

        # Set attribute if all tests passed without any exception
        self._interval_type = interval_type

    @property
    def interval_quality(self) -> str:
        """The abbreviation of its quality (e.g. augmented, perfect, ...)."""

        return self._interval_quality

    @property
    def interval_type_base_type(self) -> str:
        return WesternPitchInterval._interval_type_to_interval_base_type(
            self.interval_type
        )

    @interval_quality.setter
    def interval_quality(self, interval_quality: str):
        # Test if interval_quality string is allowed
        self._raise_error_if_interval_quality_is_invalid(interval_quality)
        self._raise_error_if_interval_quality_and_interval_type_do_not_fit(
            interval_quality, self.interval_type
        )

        # If all tests passed we can set the new interval quality
        self._interval_quality = interval_quality

    @property
    def interval_type_cent_deviation(self) -> float:
        """Get cent deviation defined by the interval type."""

        interval_base_type = WesternPitchInterval._interval_type_to_interval_base_type(
            self.interval_type
        )
        octave_count = WesternPitchInterval._interval_type_to_octave_count(
            self.interval_type
        )
        return music_parameters.constants.WESTERN_PITCH_INTERVAL_BASE_TYPE_TO_CENT_DEVIATION_DICT[
            interval_base_type
        ] + (
            music_parameters.constants.OCTAVE_IN_CENTS * octave_count
        )

    @property
    def interval_quality_cent_deviation(self) -> float:
        """Get cent deviation defined by the interval quality."""

        interval_quality_tuple = (
            self._interval_quality_string_to_interval_quality_tuple(
                self.interval_quality
            )
        )
        cent_deviation = 0
        for interval_quality in interval_quality_tuple:
            cent_deviation += music_parameters.constants.WESTERN_PITCH_INTERVAL_QUALITY_TO_CENT_DEVIATION_DICT[
                interval_quality
            ]
        # We have to make -100 for imperfect intervals if they are diminished,
        # because then they are smaller than a minor interval, which is already
        # -100.
        if (
            self.is_imperfect_interval
            and music_parameters.constants.WESTERN_PITCH_INTERVAL_QUALITY_DIMINISHED
            in interval_quality_tuple
        ):
            cent_deviation -= 100
        return cent_deviation

    @property
    def diatonic_pitch_class_count(self) -> int:
        """How many diatonic pitch classes have to be moved"""
        diatonic_pitch_class_count = int(self.interval_type) - 1
        if self.is_interval_falling:
            return -diatonic_pitch_class_count
        return diatonic_pitch_class_count

    @property
    def name(self) -> str:
        """Full interval name"""

        falling_interval_indicator = [
            "",
            music_parameters.configurations.FALLING_WESTERN_PITCH_INTERVAL_INDICATOR,
        ][self.is_interval_falling]
        return (
            f"{self.interval_quality}"
            f"{falling_interval_indicator}"
            f"{self.interval_type}"
        )

    @name.setter
    def name(self, name: str):
        self._set_attribute_by_interval_data(
            *WesternPitchInterval._interval_name_to_interval_data(name)
        )

    @property
    def is_perfect_interval(self) -> bool:
        """Return `True` if interval is perfect and otherwise `False`.

        With 'perfect' all intervals are included which can have the
        interval qualities 'augmented', 'diminished' and 'perfect'.

        This excludes intervals as sixth, thirds, ... which have
        'minor' and 'major' qualities.
        """

        return WesternPitchInterval.is_interval_type_perfect(self.interval_type)

    @property
    def is_imperfect_interval(self) -> bool:
        """Return `True` if interval is imperfect and otherwise `False`.

        With 'imperfect' all intervals are included which can have the
        interval qualities 'augmented', 'diminished', 'minor' and
        'major'.

        This excludes intervals as prime, fourth, ... which have the
        'perfect' quality.
        """

        return WesternPitchInterval.is_interval_type_imperfect(self.interval_type)

    @property
    def interval(self) -> float:
        cent_deviation = (
            self.interval_quality_cent_deviation + self.interval_type_cent_deviation
        )
        if self.is_interval_falling:
            cent_deviation = -cent_deviation
        return cent_deviation

    @property
    def semitone_count(self) -> float:
        return self.interval // 100

    @semitone_count.setter
    def semitone_count(self, semitone_count: core_constants.Real):
        self._set_attribute_by_interval_data(
            *WesternPitchInterval._semitone_count_to_interval_data(semitone_count)
        )

    @property
    def can_be_simplified(self) -> bool:
        """`True` if interval could be written in a simpler way, `False` otherwise."""

        diminished_abbreviation = music_parameters.configurations.WESTERN_PITCH_INTERVAL_QUALITY_NAME_TO_ABBREVIATION_DICT[
            music_parameters.constants.WESTERN_PITCH_INTERVAL_QUALITY_AUGMENTED
        ]
        augmented_abbreviation = music_parameters.configurations.WESTERN_PITCH_INTERVAL_QUALITY_NAME_TO_ABBREVIATION_DICT[
            music_parameters.constants.WESTERN_PITCH_INTERVAL_QUALITY_DIMINISHED
        ]

        # Special treatment for tritone which can't be written in any other way
        # but as a diminished or augmented interval
        if (
            self.interval_type_base_type == "4"
            and self.interval_quality == diminished_abbreviation
        ) or (
            self.interval_type_base_type == "5"
            and self.interval_quality == augmented_abbreviation
        ):
            return False

        # Otherwise: if there is an augmented or diminished interval
        # we can be sure it could also be written in another, simpler way.
        return any(
            [
                interval_quality in (diminished_abbreviation, augmented_abbreviation)
                for interval_quality in self.interval_quality
            ]
        )

    # ###################################################################### #
    #                           public methods                               #
    # ###################################################################### #

    @core_utilities.add_copy_option
    def inverse(self, mutate: bool = False) -> WesternPitchInterval:
        """Makes falling interval to rising and vice versa.

        **Example:**

        >>> from mutwo import music_parameters
        >>> music_parameters.WesternPitchInterval('m3').inverse()
        WesternPitchInterval('m-3')
        """
        self.is_interval_falling = not self.is_interval_falling
        return self
