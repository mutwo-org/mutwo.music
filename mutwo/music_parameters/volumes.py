"""Submodule for the parameter volume.

'Volume' is defined as any object that knows a :attr:`amplitude` attribute.
"""

import typing

import numpy as np  # type: ignore

from mutwo import core_constants
from mutwo import core_utilities
from mutwo import music_parameters

__all__ = ("DirectVolume", "DecibelVolume", "WesternVolume")


class DirectVolume(music_parameters.abc.Volume):
    """A simple volume class that gets directly initialised by its amplitude.

    :param amplitude: The amplitude of the :class:`DirectVolume` object.

    May be used when a converter class needs a volume object, but there is
    no need or desire for a complex abstraction of the respective volume.
    """

    def __init__(self, amplitude: core_constants.Real):
        self._amplitude = amplitude

    @property
    def amplitude(self) -> core_constants.Real:
        return self._amplitude

    def __repr__(self) -> str:
        return "{}({})".format(type(self).__name__, self.amplitude)


class DecibelVolume(music_parameters.abc.Volume):
    """A simple volume class that gets directly initialised by decibel.

    :param decibel: The decibel of the :class:`DecibelVolume` object (should be
        from -120 to 0).

    May be used when a converter class needs a volume object, but there is
    no need or desire for a complex abstraction of the respective volume.
    """

    def __init__(self, decibel: core_constants.Real):
        self._decibel = decibel

    @property
    def decibel(self) -> core_constants.Real:
        return self._decibel

    @property
    def amplitude(self) -> core_constants.Real:
        return self.decibel_to_amplitude_ratio(self.decibel)

    def __repr__(self) -> str:
        return "{}({})".format(type(self).__name__, self.amplitude)


class WesternVolume(music_parameters.abc.Volume):
    """Volume with a traditional Western nomenclature.

    :param name: Dynamic indicator in traditional Western nomenclature
        ('f', 'pp', 'mf', 'sfz', etc.). For a list of all supported
        indicators, see :const:`mutwo.music_parameters.constants.DYNAMIC_INDICATOR_TUPLE`.
    :type name: str
    :param minimum_decibel: The decibel value which is equal to the lowest dynamic indicator
        (ppppp).
    :type minimum_decibel: core_constants.Real, optional
    :param maximum_decibel: The decibel value which is equal to the highest dynamic indicator
        (fffff).
    :type maximum_decibel: core_constants.Real, optional

    **Example:**

    >>> from mutwo.music_parameters import volumes
    >>> volumes.WesternVolume('fff')
    WesternVolume(fff)
    """

    def __init__(
        self,
        name: str,
        minimum_decibel: typing.Optional[core_constants.Real] = None,
        maximum_decibel: typing.Optional[core_constants.Real] = None,
    ):
        minimum_decibel = (
            minimum_decibel
            or music_parameters.configurations.DEFAULT_MINIMUM_DECIBEL_FOR_MIDI_VELOCITY_AND_STANDARD_DYNAMIC_INDICATOR
        )

        maximum_decibel = (
            maximum_decibel
            or music_parameters.configurations.DEFAULT_MAXIMUM_DECIBEL_FOR_MIDI_VELOCITY_AND_STANDARD_DYNAMIC_INDICATOR
        )

        self.name = name
        self._standard_dynamic_indicator_to_decibel_mapping = (
            WesternVolume._make_standard_dynamic_indicator_to_value_dict(
                minimum_decibel,
                maximum_decibel,
                float,
            )
        )
        self._dynamic_indicator_to_decibel_mapping = (
            WesternVolume._make_dynamic_indicator_to_value_dict(
                self._standard_dynamic_indicator_to_decibel_mapping
            )
        )
        self._decibel_to_standard_dynamic_indicator_mapping = {
            decibel: dynamic_indicator
            for dynamic_indicator, decibel in self._standard_dynamic_indicator_to_decibel_mapping.items()
        }

    def __repr__(self) -> str:
        return f"{type(self).__name__}({self.name})"

    # ###################################################################### #
    #                      static private methods                            #
    # ###################################################################### #

    @staticmethod
    def _make_standard_dynamic_indicator_to_value_dict(
        minima: float, maxima: float, dtype: typing.Type[float] = float
    ) -> dict[str, float]:
        return {
            dynamic_indicator: decibel
            for dynamic_indicator, decibel in zip(
                music_parameters.constants.STANDARD_DYNAMIC_INDICATOR,
                np.linspace(
                    minima,
                    maxima,
                    len(music_parameters.constants.STANDARD_DYNAMIC_INDICATOR),
                    dtype=dtype,
                ),
            )
        }

    @staticmethod
    def _make_dynamic_indicator_to_value_dict(
        standard_dynamic_indicator_to_value_dict: dict[str, float]
    ) -> dict[str, float]:
        dynamic_indicator_to_value_dict = {}
        dynamic_indicator_to_value_dict.update(standard_dynamic_indicator_to_value_dict)
        for (
            special_dynamic_indicator,
            standard_dynamic_indicator,
        ) in (
            music_parameters.constants.SPECIAL_DYNAMIC_INDICATOR_TO_STANDARD_DYNAMIC_INDICATOR_DICT.items()
        ):
            dynamic_indicator_to_value_dict.update(
                {
                    special_dynamic_indicator: dynamic_indicator_to_value_dict[
                        standard_dynamic_indicator
                    ]
                }
            )
        return dynamic_indicator_to_value_dict

    # ###################################################################### #
    #                class methods (alternative constructors)                #
    # ###################################################################### #

    @classmethod
    def from_amplitude(cls, amplitude: core_constants.Real) -> "WesternVolume":
        """Initialise `WesternVolume` from amplitude ratio.

        :param amplitude: The amplitude which shall be converted to a `WesternVolume`
            object.

        >>> from mutwo.music_parameters import volumes
        >>> volumes.WesternVolume.from_amplitude(0.05)
        WesternVolume(p)
        """
        decibel = cls.amplitude_ratio_to_decibel(amplitude)
        return cls.from_decibel(decibel)

    @classmethod
    def from_decibel(cls, decibel: core_constants.Real) -> "WesternVolume":
        """Initialise `WesternVolume` from decibel.

        :param decibel: The decibel which shall be converted to a `WesternVolume`
            object.

        >>> from mutwo.music_parameters import volumes
        >>> volumes.WesternVolume.from_decibel(-24)
        WesternVolume(p)
        """
        volume_object = cls("mf")
        closest_decibel: float = core_utilities.find_closest_item(
            decibel,
            tuple(volume_object._decibel_to_standard_dynamic_indicator_mapping.keys()),
        )
        indicator = volume_object._decibel_to_standard_dynamic_indicator_mapping[
            closest_decibel
        ]
        volume_object.name = indicator
        return volume_object

    # ###################################################################### #
    #                             properties                                 #
    # ###################################################################### #

    @property
    def name(self) -> str:
        """The western nomenclature name for dynamic.

        For a list of all supported indicators, see
        :const:`mutwo.music_parameters.constants.DYNAMIC_INDICATOR_TUPLE`.
        """
        return self._name

    @name.setter
    def name(self, name: str) -> None:
        try:
            assert name in music_parameters.constants.DYNAMIC_INDICATOR_TUPLE
        except AssertionError:
            raise ValueError(
                f"unknown dynamic name '{name}'. Supported dynamic names "
                f"are '{music_parameters.constants.DYNAMIC_INDICATOR_TUPLE}'."
            )
        self._name = name

    @property
    def decibel(self) -> core_constants.Real:
        return self._dynamic_indicator_to_decibel_mapping[self.name]

    @property
    def amplitude(self) -> core_constants.Real:
        return self.decibel_to_amplitude_ratio(self.decibel)
