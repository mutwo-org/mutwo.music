import unittest

from mutwo import music_parameters


class LanguageBasedLyricTest(unittest.TestCase):
    def setUp(self):
        self.lyric_hello = music_parameters.LanguageBasedLyric("hello")
        self.lyric_how_are_you = music_parameters.LanguageBasedLyric("how are you?")

    def test_written_representation(self):
        self.assertEqual(self.lyric_hello.written_representation, "hello")
        self.assertEqual(self.lyric_how_are_you.written_representation, "how are you?")

    def test_phonetic_representation(self):
        self.assertEqual(self.lyric_hello.phonetic_representation, "h@l@U")
        self.assertEqual(self.lyric_how_are_you.phonetic_representation, "haU A: ju:")


class LanguageBasedSyllable(unittest.TestCase):
    def setUp(self):
        self.syllable_hel = music_parameters.LanguageBasedSyllable(False, "hel")
        self.syllable_lo = music_parameters.LanguageBasedSyllable(True, "lo")

    def test_written_representation(self):
        self.assertEqual(self.syllable_hel.written_representation, "hel")
        self.assertEqual(self.syllable_lo.written_representation, "lo")

    def test_phonetic_representation(self):
        self.assertEqual(self.syllable_hel.phonetic_representation, "he5")
        self.assertEqual(self.syllable_lo.phonetic_representation, "l@U")


if __name__ == "__main__":
    unittest.main()
