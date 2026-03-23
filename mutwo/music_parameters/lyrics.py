"""Submodule for the lyric parameter."""

from mutwo import music_parameters
from mutwo.music_parameters.constants import LYRIC_TIE, LYRIC_SUSTAIN

__all__ = ("DirectLyric", "NotationLyric")


class DirectLyric(music_parameters.abc.Lyric):
    def __init__(self, text: str, ties_previous: bool = False, ties_next: bool = False):
        self.text = text
        self.ties_previous = ties_previous
        self.ties_next = ties_next

    @property
    def text(self):
        return self._text

    @text.setter
    def text(self, text: str):
        self._text = text

    @property
    def ties_previous(self):
        return self._ties_previous

    @ties_previous.setter
    def ties_previous(self, ties_previous: bool):
        self._ties_previous = ties_previous

    @property
    def ties_next(self):
        return self._ties_next

    @ties_next.setter
    def ties_next(self, ties_next: bool):
        self._ties_next = ties_next


class NotationLyric(music_parameters.abc.Lyric):
    def __init__(self, notation: str):
        self.notation = notation

    @property
    def notation(self) -> str:
        return self._notation

    @notation.setter
    def notation(self, notation: str):
        notation = notation.strip()
        self._validate(notation)
        self._notation = notation

    def _validate(self, notation: str):
        if notation == "":
            return
        token_list = notation.split()
        if token_list == [LYRIC_SUSTAIN]:
            return
        if LYRIC_SUSTAIN in token_list and token_list != [LYRIC_SUSTAIN]:
            raise ValueError("__ must stand alone")
        if token_list.count(LYRIC_TIE) > 2:
            raise ValueError("Too many '--' tokens")
        if LYRIC_TIE in token_list[1:-1]:
            raise ValueError("'--' may only appear at edges")

    def _strip(self, notation: str) -> str:
        if notation == LYRIC_SUSTAIN:
            return ""
        if notation.startswith(LYRIC_TIE):
            notation = notation[len(LYRIC_TIE) :].lstrip()
        if notation.endswith(LYRIC_TIE):
            notation = notation[: -len(LYRIC_TIE)].rstrip()
        return notation

    def _encode(self, text, ties_previous, ties_next):
        if text == "" and ties_previous and ties_next:
            return LYRIC_SUSTAIN
        token_list = []
        if ties_previous:
            token_list.append(LYRIC_TIE)
        if text:
            token_list.append(text)
        if ties_next:
            token_list.append(LYRIC_TIE)
        return " ".join(token_list)

    def _token_list(self):
        return self.notation.split()

    @property
    def text(self) -> str:
        token_list = self._token_list()
        if token_list == [LYRIC_SUSTAIN]:
            return ""
        filtered = [t for t in token_list if t != LYRIC_TIE]
        return " ".join(filtered)

    @property
    def ties_previous(self) -> bool:
        token_list = self._token_list()
        if token_list == [LYRIC_SUSTAIN]:
            return True
        return token_list and token_list[0] == LYRIC_TIE

    @ties_previous.setter
    def ties_previous(self, value: bool):
        if self.notation == LYRIC_SUSTAIN and not value:
            raise ValueError("Cannot unset ties_previous on sustain '__'")
        self.notation = self._encode(
            self.text,
            value,
            self.ties_next,
        )

    @property
    def ties_next(self) -> bool:
        token_list = self._token_list()
        if token_list == [LYRIC_SUSTAIN]:
            return True
        return token_list and token_list[-1] == LYRIC_TIE

    @ties_next.setter
    def ties_next(self, value: bool):
        if self.notation == LYRIC_SUSTAIN and not value:
            raise ValueError("Cannot unset ties_next on sustain '__'")
        self.notation = self._encode(
            self.text,
            self.ties_previous,
            value,
        )
