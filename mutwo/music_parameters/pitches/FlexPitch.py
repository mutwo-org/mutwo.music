from __future__ import annotations

from typing import Union

from mutwo import core_parameters
from mutwo import music_parameters

__all__ = ("FlexPitch",)


class FlexPitch(music_parameters.abc.Pitch, core_parameters.abc.FlexParameterMixin):
    """A flexible pitch.

    This can be used to create dynamically changing pitches (e.g. glissandi,
    portamenti, ...).

    **Example:**

    >>> from mutwo import music_parameters
    >>> p = music_parameters.FlexPitch([[0, 'f4'], [1, 'c4']])
    """

    @classmethod
    @property
    def parameter_name(cls) -> str:
        return "pitch"

    @classmethod
    @property
    def default_parameter(cls) -> music_parameters.abc.Pitch:
        return music_parameters.DirectPitch(
            music_parameters.configurations.DEFAULT_CONCERT_PITCH
        )

    @property
    def hertz(self):
        return self.value_at(0)

    def add(self, pitch_interval: music_parameters.abc.PitchInterval.Type) -> FlexPitch:
        pitch_interval = music_parameters.abc.PitchInterval.from_any(pitch_interval)
        for pitch in self.parameter_tuple:
            pitch.add(pitch_interval)
        return self

    def __add__(
        self, other: Union[music_parameters.abc.PitchInterval.Type, list]
    ) -> FlexPitch:
        match other:
            case list():
                return core_parameters.abc.FlexParameterMixin.__add__(self, other)
            case _:
                return music_parameters.abc.Pitch.__add__(self, other)
