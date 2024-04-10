from __future__ import annotations

from mutwo import core_constants
from mutwo import music_parameters

__all__ = ("DirectPitch",)


class DirectPitch(music_parameters.abc.Pitch):
    """A simple pitch class that gets directly initialised by its frequency.

    :param hertz: The hertz of the ``DirectPitch`` object.

    May be used when a converter class needs a pitch object, but there is
    no need or desire for a complex abstraction of the respective pitch
    (that classes like ``JustIntonationPitch`` or ``WesternPitch`` offer).

    **Example:**

    >>> from mutwo import music_parameters
    >>> my_pitch = music_parameters.DirectPitch(440)
    """

    def __init__(self, hertz: core_constants.Real, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._hertz = float(hertz)

    @property
    def hertz(self) -> float:
        """The frequency of the pitch."""
        return self._hertz

    def __repr__(self) -> str:
        return "DirectPitch(hertz = {})".format(self.hertz)

    def add(self, pitch_interval: music_parameters.abc.PitchInterval) -> DirectPitch:
        self._hertz = self.cents_to_ratio(pitch_interval.cents) * self.hertz
        return self
