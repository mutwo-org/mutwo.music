"""Event classes which are designated for musical usage."""

from . import configurations

from .music import *

from . import music

__all__ = music.__all__

# Force flat structure
del music
