import typing

import phonemizer

from mutwo import music_parameters


__all__ = ("LanguageBasedLyric", "LanguageBasedSyllable")


class LanguageBasedLyric(music_parameters.abc.Lyric):
    """Lyric based on a natural language.

    :param written_representation: The text.
    :type written_representation: str
    :param language_code: The code for the language of the text.
        If this is `None` the constant
        `mutwo.music_parameters.configurations.DEFAULT_LANGUAGE_CODE`
        will be used. Default to `None`.
    :type language_code: typing.Optional[str]
    """

    _language_code_tuple = (
        phonemizer.backend.EspeakMbrolaBackend._all_supported_languages()
    )

    def __init__(
        self, written_representation: str, language_code: typing.Optional[str] = None
    ):
        if language_code is None:
            language_code = music_parameters.configurations.DEFAULT_LANGUAGE_CODE

        self.written_representation = written_representation
        self.language_code = language_code

    @property
    def language_code(self) -> str:
        return self._language_code

    @language_code.setter
    def language_code(self, language_code: str):
        try:
            assert language_code in self._language_code_tuple
        except AssertionError:
            raise ValueError(
                (
                    f"Found invalid language code '{language_code}'. "
                    "Please use one of the supported language codes: \n\n"
                    f"{self._language_code_tuple}"
                )
            )
        self._language_code = language_code

    @property
    def written_representation(self) -> str:
        return self._written_representation

    @written_representation.setter
    def written_representation(self, written_representation: str):
        self._written_representation = written_representation

    @property
    def phonetic_representation(self) -> str:
        word_tuple = self.written_representation.split(" ")
        return " ".join(
            [
                phonemizer.phonemize(
                    word, backend="espeak-mbrola", language=self.language_code
                )
                for word in word_tuple
            ]
        )


class LanguageBasedSyllable(music_parameters.abc.Syllable, LanguageBasedLyric):
    """Syllable based on a natural language.

    :param is_last_syllable: `True` if it is the last syllable of a word and
        `False` if it isn't the last syllable
    :type is_last_syllable: bool
    :param written_representation: The text.
    :type written_representation: str
    :param language_code: The code for the language of the text.
        If this is `None` the constant
        `mutwo.music_parameters.configurations.DEFAULT_LANGUAGE_CODE`
        will be used. Default to `None`.
    :type language_code: typing.Optional[str]

    **Warning:**

    It is a known bug that a split word (syllables) and the word
    itself will return different values for :attr:`phonetic_representation`.
    For instance:

    >>> LanguageBasedLyric('hello').phonetic_representation
    "h@l@U"
    >>> # And now splitted to syllables:
    >>> LanguageBasedSyllable('hel').phonetic_representation
    "he5"
    >>> LanguageBasedSyllable('lo').phonetic_representation
    "l@U"
    """

    def __init__(self, is_last_syllable: bool, *args, **kwargs):
        music_parameters.abc.Syllable.__init__(self, is_last_syllable)
        LanguageBasedLyric.__init__(self, *args, **kwargs)
