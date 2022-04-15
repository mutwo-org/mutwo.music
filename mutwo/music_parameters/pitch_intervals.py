from mutwo import music_parameters

__all__ = ("DirectPitchInterval",)


class DirectPitchInterval(music_parameters.abc.PitchInterval):
    """Simple interval class which gets directly assigned by its cents value

    :param interval: Defines how big or small the interval is in cents.
    :type interval: float
    """

    def __init__(self, interval: float):
        self.interval = interval

    @property
    def interval(self) -> float:
        return self._interval

    @interval.setter
    def interval(self, interval: float):
        self._interval = interval



class WesternPitchInterval(music_parameters.abc.PitchInterval):
    pass
