import unittest

from mutwo import music_converters
from mutwo import music_parameters


class ImproveWesternPitchListSequenceReadabilityTest(unittest.TestCase):
    def setUp(self):
        self.improve_western_pitch_list_sequence_readability = (
            music_converters.ImproveWesternPitchListSequenceReadability()
        )

    def test_convert_simple(self):
        self.assertEqual(
            self.improve_western_pitch_list_sequence_readability.convert(
                [
                    [
                        music_parameters.WesternPitch("c"),
                        music_parameters.WesternPitch("dss"),
                        music_parameters.WesternPitch("g"),
                    ]
                ]
            ),
            (
                [
                    music_parameters.WesternPitch("c"),
                    music_parameters.WesternPitch("e"),
                    music_parameters.WesternPitch("g"),
                ],
            ),
        )


if __name__ == "__main__":
    unittest.main()
