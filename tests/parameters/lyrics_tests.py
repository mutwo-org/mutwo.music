import unittest

from mutwo import music_parameters


class LanguageBasedLyricTest(unittest.TestCase):
    def setUp(self):
        self.lyric_hello = music_parameters.LanguageBasedLyric("hallo")
        self.lyric_how_are_you = music_parameters.LanguageBasedLyric("wie geht es dir?")

    def test_written_representation(self):
        self.assertEqual(self.lyric_hello.written_representation, "hallo")
        self.assertEqual(self.lyric_how_are_you.written_representation, "wie geht es dir?")

    def test_phonetic_representation(self):
        self.assertEqual(self.lyric_hello.phonetic_representation, "halo:")
        self.assertEqual(self.lyric_how_are_you.phonetic_representation, "vi:@ ge:t e:s di:R\\")


class LanguageBasedSyllable(unittest.TestCase):
    def setUp(self):
        self.syllable_hel = music_parameters.LanguageBasedSyllable(False, "hal")
        self.syllable_lo = music_parameters.LanguageBasedSyllable(True, "lo")

    def test_written_representation(self):
        self.assertEqual(self.syllable_hel.written_representation, "hal")
        self.assertEqual(self.syllable_lo.written_representation, "lo")

    def test_phonetic_representation(self):
        self.assertEqual(self.syllable_hel.phonetic_representation, "hA:l")
        self.assertEqual(self.syllable_lo.phonetic_representation, "lo:")


if __name__ == "__main__":
    unittest.main()
