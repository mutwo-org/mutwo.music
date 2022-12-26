from . import constants
from . import configurations
from . import abc

from .ambituses import *
from .commas import *
from .lyrics import *
from .pitch_intervals import *
from .pitches import *
from .scales import *

# instruments need configurations. We can't load configurations
# in mutwo.music_parameters.configurations.__init__.py, because
# we use objects there which aren't available yet.
from mutwo.music_parameters.configurations import instruments
configurations.__dict__.update(instruments.__dict__)
del instruments

from .instruments import *  # needs pitches

from .volumes import *
from .notation_indicators import *
from .playing_indicators import *

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
