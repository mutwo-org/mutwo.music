"""Submodule for the parameter pitch.

'Pitch' is defined as any object that knows a :attr:`frequency` attribute.
The two major modern tuning systems Just intonation and Equal-divided-octave
are supported by the :class:`JustIntonationPitch` and :class:`EqualDividedOctavePitch` classes.
For using Western nomenclature (e.g. c, d, e, f, ...) :mod:`mutwo` offers the
:class:`WesternPitch` class (which inherits from :class:`EqualDividedOctavePitch`).
For a straight frequency-based approach one may use :class:`DirectPitch`.

If desired the default concert pitch can be adjusted after importing :mod:`mutwo`:

    >>> from mutwo import music_parameters
    >>> music_parameters.configurations.DEFAULT_CONCERT_PITCH = 443

All pitch objects with a concert pitch attribute that become initialised after
overriding the default concert pitch value will by default use the new
overridden default concert pitch value.
"""


from .DirectPitch import *
from .MidiPitch import *
from .JustIntonationPitch import *
from .CommonHarmonic import *
from .EqualDividedOctavePitch import *
from .WesternPitch import *


__all__ = (
    "DirectPitch",
    "JustIntonationPitch",
    "Partial",
    "EqualDividedOctavePitch",
    "WesternPitch",
    "MidiPitch",
    "CommonHarmonic",
)
