from . import configurations

from .parsers import *
from .grace_notes import *
from .metricities import *
from .playing_indicators import *
from .spectrals import *

from . import (
    grace_notes,
    metricities,
    parsers,
    playing_indicators,
    spectrals,
)

from mutwo import core_utilities

__all__ = core_utilities.get_all(
    grace_notes,
    metricities,
    parsers,
    playing_indicators,
    spectrals,
)

# Force flat structure
del (
    core_utilities,
    grace_notes,
    metricities,
    parsers,
    playing_indicators,
    spectrals,
)
