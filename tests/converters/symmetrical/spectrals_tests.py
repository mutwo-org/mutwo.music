import unittest

from mutwo import music_converters
from mutwo import music_parameters


class TwoPitchesToCommonHarmonicsTest(unittest.TestCase):
    def test_convert(self):
        converter = music_converters.TwoPitchesToCommonHarmonics(True, 1, 16)

        self.assertEqual(
            converter.convert(
                (
                    music_parameters.JustIntonationPitch("7/4"),
                    music_parameters.JustIntonationPitch(),
                )
            ),
            (
                music_parameters.CommonHarmonic(
                    (
                        music_parameters.Partial(1, True),
                        music_parameters.Partial(7, True),
                    ),
                    "7/1",
                ),
                music_parameters.CommonHarmonic(
                    (
                        music_parameters.Partial(2, True),
                        music_parameters.Partial(14, True),
                    ),
                    "14/1",
                ),
            ),
        )


if __name__ == "__main__":
    unittest.main()
