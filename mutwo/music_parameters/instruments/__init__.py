"""Representations for musical instruments"""

__all__ = (
    "UnpitchedInstrument",
    "ContinuousPitchedInstrument",
    "DiscreetPitchedInstrument",
    "Orchestration",
    "OrchestrationMixin",
    "CelticHarp",
    "Piccolo",
    "Flute",
    "Oboe",
    "BfClarinet",
    "EfClarinet",
    "Bassoon",
)

from .general import (
    UnpitchedInstrument,
    ContinuousPitchedInstrument,
    DiscreetPitchedInstrument,
    Orchestration,
    OrchestrationMixin,
)
from .CelticHarp import CelticHarp
from .Piccolo import Piccolo
from .Flute import Flute
from .Oboe import Oboe
from .BfClarinet import BfClarinet
from .EfClarinet import EfClarinet
from .Bassoon import Bassoon
