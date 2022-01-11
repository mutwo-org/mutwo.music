import unittest

from mutwo.ext import converters
from mutwo.ext import parameters as ext_parameters


class TwoPitchesToCommonHarmonicsConverterTest(unittest.TestCase):
    def test_convert(self):
        converter = (
            converters.symmetrical.spectrals.TwoPitchesToCommonHarmonicsConverter(
                True, 1, 16
            )
        )

        self.assertEqual(
            converter.convert(
                (
                    ext_parameters.pitches.JustIntonationPitch("7/4"),
                    ext_parameters.pitches.JustIntonationPitch(),
                )
            ),
            (
                ext_parameters.pitches.CommonHarmonic(
                    (
                        ext_parameters.pitches.Partial(1, True),
                        ext_parameters.pitches.Partial(7, True),
                    ),
                    "7/1",
                ),
                ext_parameters.pitches.CommonHarmonic(
                    (
                        ext_parameters.pitches.Partial(2, True),
                        ext_parameters.pitches.Partial(14, True),
                    ),
                    "14/1",
                ),
            ),
        )


if __name__ == "__main__":
    unittest.main()
