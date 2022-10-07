"""Define lyrics to be sung, spoken or written"""

from mutwo import music_parameters

from .text_based_lyrics import *

__all__ = ("DirectLyric",) + text_based_lyrics.__all__

del text_based_lyrics



class DirectLyric(music_parameters.abc.Lyric):
    """Lyric which is directly initialised by its phonetic representation

    :param phonetic_representation: The phonetic representation of
        the text.
    :type phonetic_representation: str

    In this class the `written_representation` is simply equal to
    `phonetic_representation`.
    """

    def __init__(self, phonetic_representation: str):
        self.phonetic_representation = phonetic_representation

    @property
    def phonetic_representation(self) -> str:
        return self._phonetic_representation

    @phonetic_representation.setter
    def phonetic_representation(self, phonetic_representation: str):
        self._phonetic_representation = phonetic_representation

    @property
    def written_representation(self) -> str:
        return self.phonetic_representation
