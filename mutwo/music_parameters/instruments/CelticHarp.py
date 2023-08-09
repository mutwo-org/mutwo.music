from __future__ import annotations

from mutwo import music_parameters

from .general import DiscreetPitchedInstrument, _setdefault


class CelticHarp(DiscreetPitchedInstrument):
    """A typical beginners harp without any pedals."""

    def __init__(self, **kwargs):
        super().__init__(
            **_setdefault(
                kwargs, music_parameters.configurations.DEFAULT_CELTIC_HARP_DICT
            )
        )
