import unittest

from mutwo import music_parameters


class LanguageBasedLyricTest(unittest.TestCase):
    def setUp(self):
        self.lyric_hello = music_parameters.LanguageBasedLyric("hallo")
        self.lyric_how_are_you = music_parameters.LanguageBasedLyric("wie geht es dir?")

    def test_written_representation(self):
        self.assertEqual(self.lyric_hello.written_representation, "hallo")
        self.assertEqual(self.lyric_how_are_you.written_representation, "wie geht es dir?")

    def test_xsampa(self):
        self.assertEqual(self.lyric_hello.xsampa, "halo:")
        self.assertEqual(self.lyric_how_are_you.xsampa, "vi:@ ge:t e:s di:R\\")


class LanguageBasedSyllable(unittest.TestCase):
    def setUp(self):
        self.syllable_hel = music_parameters.LanguageBasedSyllable(False, "hal")
        self.syllable_lo = music_parameters.LanguageBasedSyllable(True, "lo")

    def test_written_representation(self):
        self.assertEqual(self.syllable_hel.written_representation, "hal")
        self.assertEqual(self.syllable_lo.written_representation, "lo")

    def test_xsampa(self):
        self.assertEqual(self.syllable_hel.xsampa, "hA:l")
        self.assertEqual(self.syllable_lo.xsampa, "lo:")


if __name__ == "__main__":
    unittest.main()
