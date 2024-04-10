"""Define lyrics to be sung, spoken or written"""

from mutwo import music_parameters

from .text_based_lyrics import *

__all__ = ("DirectLyric",) + text_based_lyrics.__all__

del text_based_lyrics



class DirectLyric(music_parameters.abc.Lyric):
    """Lyric which is directly initialised by its phonetic representation

    :param xsampa: The phonetic representation of
        the text.
    :type xsampa: str

    In this class the `written_representation` is simply equal to
    `xsampa`.
    """

    def __init__(self, xsampa: str):
        self.xsampa = xsampa

    @property
    def xsampa(self) -> str:
        return self._xsampa

    @xsampa.setter
    def xsampa(self, xsampa: str):
        self._xsampa = xsampa

    @property
    def written_representation(self) -> str:
        return self.xsampa
