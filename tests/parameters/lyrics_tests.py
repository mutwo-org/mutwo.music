import unittest

from mutwo import music_parameters
from mutwo.music_parameters.constants import LYRIC_TIE, LYRIC_SUSTAIN


class DirectLyricTest(unittest.TestCase):
    def test_basic_assignment(self):
        lyric = music_parameters.DirectLyric("hello", False, True)

        self.assertEqual(lyric.text, "hello")
        self.assertFalse(lyric.ties_previous)
        self.assertTrue(lyric.ties_next)

        lyric.text = "world"
        self.assertEqual(lyric.text, "world")

        lyric.ties_previous = True
        self.assertTrue(lyric.ties_previous)


class NotationLyricTest(unittest.TestCase):
    def test_empty_notation(self):
        lyric = music_parameters.NotationLyric("")
        self.assertEqual(lyric.text, "")
        self.assertFalse(lyric.ties_previous)
        self.assertFalse(lyric.ties_next)

    def test_sustain(self):
        lyric = music_parameters.NotationLyric(LYRIC_SUSTAIN)
        self.assertEqual(lyric.text, "")
        self.assertTrue(lyric.ties_previous)
        self.assertTrue(lyric.ties_next)

    def test_simple_word(self):
        lyric = music_parameters.NotationLyric("hello")
        self.assertEqual(lyric.text, "hello")
        self.assertFalse(lyric.ties_previous)
        self.assertFalse(lyric.ties_next)

    def test_prefix_tie(self):
        lyric = music_parameters.NotationLyric(f"{LYRIC_TIE} hello")
        self.assertEqual(lyric.text, "hello")
        self.assertTrue(lyric.ties_previous)
        self.assertFalse(lyric.ties_next)

    def test_suffix_tie(self):
        lyric = music_parameters.NotationLyric(f"hello {LYRIC_TIE}")
        self.assertEqual(lyric.text, "hello")
        self.assertFalse(lyric.ties_previous)
        self.assertTrue(lyric.ties_next)

    def test_both_ties(self):
        lyric = music_parameters.NotationLyric(f"{LYRIC_TIE} hello {LYRIC_TIE}")
        self.assertEqual(lyric.text, "hello")
        self.assertTrue(lyric.ties_previous)
        self.assertTrue(lyric.ties_next)

    def test_invalid_middle_tie(self):
        with self.assertRaises(ValueError):
            music_parameters.NotationLyric(f"hel {LYRIC_TIE} lo")

    def test_setters_modify_notation(self):
        lyric = music_parameters.NotationLyric("hello")

        lyric.ties_previous = True
        self.assertTrue(lyric.ties_previous)

        lyric.ties_next = True
        self.assertTrue(lyric.ties_next)

    def test_roundtrip_consistency(self):
        original = f"{LYRIC_TIE} hello {LYRIC_TIE}"
        lyric = music_parameters.NotationLyric(original)

        self.assertEqual(lyric.text, "hello")
        self.assertTrue(lyric.ties_previous)
        self.assertTrue(lyric.ties_next)


if __name__ == "__main__":
    unittest.main()
