from __future__ import annotations
import typing

from mutwo import core_utilities

__all__ = (
    "DIATONIC_PITCH_CLASS_CONTAINER",
    "DIATONIC_PITCH_CLASS_NAME_PAIR_TO_COMPENSATION_IN_CENTS_DICT",
    "OCTAVE_IN_CENTS",
)


def get_diatonic_pitch_class_name_pair_to_compensation_in_cents() -> dict[
    tuple[str, str], float
]:
    from mutwo import core_utilities

    reference_tuple = tuple(
        diatonic_pitch_class.pitch_class * 100
        for diatonic_pitch_class in DIATONIC_PITCH_CLASS_CONTAINER
    )

    diatonic_pitch_class_name_pair_to_compensation_in_cents = {}
    for scale in core_utilities.cyclic_permutations(
        DIATONIC_PITCH_CLASS_CONTAINER.as_tuple()
    ):
        root_diatonic_pitch_class = scale[0]
        for reference, diatonic_pitch_class in zip(reference_tuple, scale):
            cent_difference = (
                diatonic_pitch_class.pitch_class - root_diatonic_pitch_class.pitch_class
            ) * 100
            if cent_difference < 0:
                cent_difference += OCTAVE_IN_CENTS
            difference_to_reference = reference - cent_difference
            diatonic_pitch_class_name_pair_to_compensation_in_cents.update(
                {
                    (
                        root_diatonic_pitch_class.as_string(),
                        diatonic_pitch_class.as_string(),
                    ): difference_to_reference
                }
            )

    return diatonic_pitch_class_name_pair_to_compensation_in_cents


OCTAVE_IN_CENTS = 1200
"""How many cents equal one octave"""

ASCENDING_DIATONIC_PITCH_CLASS_NAME_TUPLE = "c d e f g a b".split(" ")

ASCENDING_DIATONIC_PITCH_CLASS_NUMBER_TUPLE = (0, 2, 4, 5, 7, 9, 11)

DIATONIC_PITCH_NAME_TO_PITCH_CLASS_DICT = {
    diatonic_pitch_name: pitch_class
    for diatonic_pitch_name, pitch_class in zip(
        ASCENDING_DIATONIC_PITCH_CLASS_NAME_TUPLE,
        ASCENDING_DIATONIC_PITCH_CLASS_NUMBER_TUPLE,
    )
}

DIATONIC_PITCH_CLASS_COUNT = len(ASCENDING_DIATONIC_PITCH_CLASS_NAME_TUPLE)


class DiatonicPitchClass(str):
    """Represent a diatonic pitch class"""

    DiatonicStepCount = int
    OctaveCount = int

    # Prohibit dynamic attribute allocation
    __slots__ = (
        "__pitch_class",
        "__index",
        "__diatonic_pitch_class_name",
    )

    def __new__(cls, diatonic_pitch_class_name: str, _: int, __: int):
        diatonic_pitch_class = str.__new__(cls, diatonic_pitch_class_name)
        return diatonic_pitch_class

    def __init__(self, diatonic_pitch_class_name: str, pitch_class: int, index: int):
        # Strict read only!
        self.__diatonic_pitch_class_name = diatonic_pitch_class_name
        self.__pitch_class = pitch_class
        self.__index = index

    def __add__(
        self, diatonic_step_count: DiatonicStepCount
    ) -> tuple[DiatonicPitchClass, OctaveCount]:
        """Add diatonic step count to diatonic pitch class"""

        new_index = self.index + diatonic_step_count
        new_diatonic_pitch_class = (
            DIATONIC_PITCH_CLASS_CONTAINER.get_diatonic_pitch_class_by(
                index=self._unlimited_index_to_index(new_index)
            )
        )
        octave_count = self._unlimited_index_to_octave_count(new_index)
        return new_diatonic_pitch_class, octave_count

    def __sub__(
        self, diatonic_pitch_class: DiatonicPitchClass
    ) -> tuple[DiatonicStepCount, OctaveCount]:
        """Get diatonic step count between itself and other diatonic pitch class"""

        index_self, index_other = self.index, diatonic_pitch_class.index
        difference = index_self - index_other
        diatonic_step_count, octave_count = (
            self._unlimited_index_to_index(difference),
            self._unlimited_index_to_octave_count(difference),
        )
        return diatonic_step_count, octave_count

    @staticmethod
    def _unlimited_index_to_index(unlimited_index: int) -> int:
        return unlimited_index % DIATONIC_PITCH_CLASS_COUNT

    @staticmethod
    def _unlimited_index_to_octave_count(unlimited_index: int) -> int:
        return unlimited_index // DIATONIC_PITCH_CLASS_COUNT

    @property
    def pitch_class(self) -> int:
        """Return pitch class as number"""
        return self.__pitch_class

    @property
    def index(self) -> int:
        return self.__index

    @property
    def neighbour_tuple(
        self,
    ) -> tuple[
        tuple[DiatonicPitchClass, OctaveCount], tuple[DiatonicPitchClass, OctaveCount]
    ]:
        neighbour_list = []
        for value in (-1, 1):
            unlimited_index = self.index + value
            index, octave_count = self._unlimited_index_to_index(
                unlimited_index
            ), self._unlimited_index_to_octave_count(unlimited_index)
            diatonic_pitch = DIATONIC_PITCH_CLASS_CONTAINER.get_diatonic_pitch_class_by(
                index=index
            )
            neighbour_list.append((diatonic_pitch, octave_count))
        return tuple(neighbour_list)

    def as_string(self) -> str:
        return self.__diatonic_pitch_class_name


class DiatonicPitchClassContainer(object):
    """Singleton which includes all diatonic pitch classes"""

    # We use slots to prohibit dynamic attribute allocation. This
    # is a real singleton and nothing of it should be changed.
    __slots__ = tuple(ASCENDING_DIATONIC_PITCH_CLASS_NAME_TUPLE)

    def __new__(cls, *args, **kwargs) -> DiatonicPitchClassContainer:
        for (index, diatonic_pitch_class_name) in enumerate(
            ASCENDING_DIATONIC_PITCH_CLASS_NAME_TUPLE
        ):
            pitch_class = DIATONIC_PITCH_NAME_TO_PITCH_CLASS_DICT[
                diatonic_pitch_class_name
            ]
            # We can't just use a simple lambda function,
            # because python would mess up the local variables.
            get_diatonic_pitch_class = type(
                f"get_{diatonic_pitch_class_name}",
                (object,),
                {
                    "_diatonic_pitch_class": DiatonicPitchClass(
                        diatonic_pitch_class_name,
                        pitch_class,
                        index,
                    ),
                    "__call__": lambda self, *_, **__: self._diatonic_pitch_class,
                },
            )()
            setattr(cls, diatonic_pitch_class_name, property(get_diatonic_pitch_class))
        return object.__new__(cls, *args, **kwargs)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def as_tuple(self) -> tuple[DiatonicPitchClass, ...]:
        return tuple(
            getattr(self, diatonic_pitch_class_name)
            for diatonic_pitch_class_name in ASCENDING_DIATONIC_PITCH_CLASS_NAME_TUPLE
        )

    @property
    def diatonic_pitch_class_count(self) -> int:
        return DIATONIC_PITCH_CLASS_COUNT

    def __getitem__(
        self, key_or_index_or_slice: str | int | slice
    ) -> DiatonicPitchClass | tuple[DiatonicPitchClass, ...]:
        if isinstance(key_or_index_or_slice, str):
            return getattr(self, key_or_index_or_slice)
        return self.as_tuple()[key_or_index_or_slice]

    def __iter__(self) -> typing.Iterator[DiatonicPitchClass]:
        return iter(self.as_tuple())

    def get_diatonic_pitch_class_by(
        self, **attribute_name_and_expected_value
    ) -> DiatonicPitchClass:
        """Query diatonic pitch classes and find first suitable candidate

        :param attribute_name_and_expected_value: Should be the attribute name
            of a :class:`DiatonicPitchClass` and its expected value.
        """
        candidate_list = []
        for diatonic_pitch_class in self:
            is_allowed = True
            for attribute, value in attribute_name_and_expected_value.items():
                if getattr(diatonic_pitch_class, attribute) != value:
                    is_allowed = False
                    break
            if is_allowed:
                candidate_list.append(diatonic_pitch_class)
        if candidate_list:
            return candidate_list[0]
        raise Exception(
            "Couldn't find DiatonicPitchClass with query "
            f"'{attribute_name_and_expected_value}'"
        )

    def get_closest_diatonic_pitch_class(
        self, pitch_class: float
    ) -> DiatonicPitchClass:
        """Find the closest diatonic pitch class to the given pitch class

        :param pitch_class: The pitch class number for which the closest
            diatonic pitch shall be found.
        :type pitch_class: float
        :return: A :class:`DiatonicPitchClass` object.

        **Example:**

        >>> from mutwo import music_parameters
        >>> music_parameters.constants.DIATONIC_PITCH_CLASS_CONTAINER.get_closest_diatonic_pitch_class(2)
        'd'
        """

        return core_utilities.find_closest_item(
            pitch_class,
            self.as_tuple(),
            key=lambda diatonic_pitch_class: diatonic_pitch_class.pitch_class,
        )


DIATONIC_PITCH_CLASS_CONTAINER = DiatonicPitchClassContainer()
"""This namespace / singleton includes all diatonic pitch classes as python
objects. The pitch class objects can be fetched by using their name (e.g.
`DIATONIC_PITCH_CLASS_CONTAINER.c`), by using indices or by iterating over the
container. The objects are immutable string-like objects with additional
methods and properties to simplify handling pitches with diatonic pitch
names."""


DIATONIC_PITCH_CLASS_NAME_PAIR_TO_COMPENSATION_IN_CENTS_DICT = (
    get_diatonic_pitch_class_name_pair_to_compensation_in_cents()
)
"""This dictionary maps two diatonic pitch classes to a certain
cent value. The cent value describes the difference between a major
or perfect interval and the interval which occurs between the two
diatonic pitch classes. In other words: the cent value shows the
difference between an interval between two diatonic pitches (e.g. a
sixth) and what the interval would be in a major scale between the
root note and another pitch. This dictionary is used in
:class:`mutwo.music_parameters.WesternPitch` in order to find out
a new pitch after being altered by a
:class:`muwo.music_parameters.WesternPitchInterval`."""
