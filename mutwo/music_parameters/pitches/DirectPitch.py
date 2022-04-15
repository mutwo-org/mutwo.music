from __future__ import annotations

from mutwo import core_constants
from mutwo import core_utilities
from mutwo import music_parameters

__all__ = ("DirectPitch",)


class DirectPitch(music_parameters.abc.Pitch):
    """A simple pitch class that gets directly initialised by its frequency.

    :param frequency: The frequency of the ``DirectPitch`` object.

    May be used when a converter class needs a pitch object, but there is
    no need or desire for a complex abstraction of the respective pitch
    (that classes like ``JustIntonationPitch`` or ``WesternPitch`` offer).

    **Example:**

    >>> from mutwo.music_parameters import pitches
    >>> my_pitch = pitches.DirectPitch(440)
    """

    def __init__(self, frequency: core_constants.Real, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._frequency = float(frequency)

    @property
    def frequency(self) -> float:
        """The frequency of the pitch."""

        return self._frequency

    def __repr__(self) -> str:
        return "DirectPitch(frequency = {})".format(self.frequency)

    @core_utilities.add_copy_option
    def add(
        self, pitch_interval: music_parameters.abc.PitchInterval, mutate: bool = False
    ) -> DirectPitch:
        self._frequency = self.cents_to_ratio(pitch_interval.interval) * self.frequency
        return self
