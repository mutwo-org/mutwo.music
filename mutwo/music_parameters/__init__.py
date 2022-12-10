from . import constants
from . import configurations
from . import abc

from .ambituses import *
from .commas import *
from .lyrics import *
from .pitch_intervals import *
from .pitches import *
from .instruments import *  # needs pitches
from .volumes import *
from .notation_indicators import *
from .playing_indicators import *
from .scales import *

from . import (
    ambituses,
    commas,
    instruments,
    lyrics,
    pitch_intervals,
    pitches,
    volumes,
    notation_indicators,
    playing_indicators,
    scales,
)

from mutwo import core_utilities


__all__ = core_utilities.get_all(
    ambituses,
    commas,
    instruments,
    lyrics,
    pitch_intervals,
    pitches,
    volumes,
    notation_indicators,
    playing_indicators,
    scales,
)

# Force flat structure
del (
    ambituses,
    core_utilities,
    commas,
    instruments,
    lyrics,
    pitch_intervals,
    pitches,
    volumes,
    notation_indicators,
    playing_indicators,
    scales,
)
