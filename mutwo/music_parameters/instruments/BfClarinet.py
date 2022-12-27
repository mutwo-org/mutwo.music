from mutwo import music_parameters

from .general import _setdefault, ContinuousPitchedInstrument


class BfClarinet(ContinuousPitchedInstrument):
    def __init__(self, **kwargs):
        super().__init__(
            **_setdefault(
                kwargs, music_parameters.configurations.DEFAULT_BF_CLARINET_DICT
            )
        )
