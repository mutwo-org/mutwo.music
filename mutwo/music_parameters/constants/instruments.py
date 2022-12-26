import enum


class HarpFinger(enum.IntEnum):
    """Mapping of finger to index.

    This is useful when using integers inside algorithms
    instead of :class:`mutwo.music_parameters.abc.BodyPart`
    instances.

    Note: Harp players only use first four fingers.
    """

    LeftOne = -1  # left thumb
    LeftTwo = -2  # left forefinger
    LeftThree = -3  # left long finger
    LeftFour = -4  # left annual finger

    RightOne = 1  # right thumb
    RightTwo = 2  # right forefinger
    RightThree = 3  # right long finger
    RightFour = 4  # right annual finger


del enum
