import unittest

from mutwo import music_utilities


class ToolTest(unittest.TestCase):
    def test_linear_space(self):
        s = music_utilities.linear_space

        # as tuple
        self.assertEqual(tuple(s(0, 5, 6)), (0, 1, 2, 3, 4, 5))

        # as generator
        g = s(0, 5, 6)
        self.assertEqual(0, next(g))
        self.assertEqual(1, next(g))
        self.assertEqual(2, next(g))
        self.assertEqual(3, next(g))

        # with floating point numbers
        self.assertEqual(tuple(s(0, 1, 3)), (0, 0.5, 1))
