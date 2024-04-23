from __future__ import annotations

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
