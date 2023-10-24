from __future__ import annotations

import typing

from mutwo import core_utilities
from mutwo import music_parameters

__all__ = ("ScalePitch",)


class ScalePitch(music_parameters.abc.Pitch):
    """Pitch that is defined by its scale degree, octave and reference scale.

    :param scale_degree: The scale degree of the pitch, starting from 0.
        For instance in a C major scale, the scale degree of 0 corresponds
        to the pitch "c", the scale degree 2 to the pitch "e". Default to 0.
    :type scale_degree: int
    :param octave: The octave of the pitch. Default to 0.
    :type octave: int
    :param scale: The scale to which scale degree and octave
        refer to. If set to ``None`` the default scale is used
        (`mutwo.music_parameters.configurations.DEFAULT_SCALE`).
        Default to ``None``.
    :type scale: music_parameters.Scale

    **Example:**

    >>> from mutwo import music_parameters
    >>> p = music_parameters.ScalePitch(scale_degree=1, octave=-1)
    """

    def __init__(
        self,
        scale_degree: int = 0,
        octave: int = 0,
        scale: typing.Optional[music_parameters.Scale] = None,
        *args,
        **kwargs,
    ):
        super().__init__(*args, **kwargs)
        self.scale_degree = scale_degree
        self.octave = octave
        self.scale = scale or music_parameters.configurations.DEFAULT_SCALE

    def __repr__(self) -> str:
        return (
            f"{type(self).__name__}(scale_degree = "
            f"{self.scale_degree}, octave = {self.octave})"
        )

    @property
    def scale_position(self) -> tuple[int, int]:
        return (self.scale_degree, self.octave)

    @property
    def scale_pitch(self) -> music_parameters.abc.Pitch:
        return self.scale.scale_position_to_pitch(self.scale_position)

    @property
    def frequency(self) -> float:
        return self.scale_pitch.frequency

    @core_utilities.add_copy_option
    def add(
        self, pitch_interval: music_parameters.abc.PitchInterval, mutate: bool = False
    ) -> ScalePitch:
        p = self.scale_pitch.add(pitch_interval, mutate=False)
        if p not in self.scale.pitch_tuple:
            raise RuntimeError(f"Pitch '{p}' isn't part of reference scale.")
        self.scale_degree, self.octave = self.scale.pitch_to_scale_position(p)
        return self
