import unittest


from mutwo import music_converters


class RhythmicalStrataToIndispensabilityTest(unittest.TestCase):
    def test_convert(self):
        converter = (
            music_converters.RhythmicalStrataToIndispensability()
        )

        # 3/4
        self.assertEqual(converter.convert((2, 3)), (5, 0, 3, 1, 4, 2))
        # 6/8
        self.assertEqual(converter.convert((3, 2)), (5, 0, 2, 4, 1, 3))


if __name__ == "__main__":
    unittest.main()
