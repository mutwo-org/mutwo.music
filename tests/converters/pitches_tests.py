import unittest

from mutwo import music_converters
from mutwo import music_parameters


class ImproveWesternPitchListSequenceReadabilityTest(unittest.TestCase):
    def setUp(self):
        self.improve_western_pitch_list_sequence_readability = (
            music_converters.ImproveWesternPitchListSequenceReadability()
        )

    def test_get_pitch_variant_tuple(self):
        for western_pitch, expected_pitch_variant_tuple in (
            (
                music_parameters.WesternPitch("c"),
                (
                    music_parameters.WesternPitch("c"),
                    music_parameters.WesternPitch("bs", 3),
                    music_parameters.WesternPitch("dff"),
                ),
            ),
            (
                music_parameters.WesternPitch("f"),
                (
                    music_parameters.WesternPitch("f"),
                    music_parameters.WesternPitch("es"),
                    music_parameters.WesternPitch("gff"),
                ),
            ),
            (
                music_parameters.WesternPitch("ef"),
                (
                    music_parameters.WesternPitch("ef"),
                    music_parameters.WesternPitch("ds"),
                    music_parameters.WesternPitch("fff"),
                ),
            ),
        ):
            self.assertEqual(
                music_converters.ImproveWesternPitchListSequenceReadability._get_pitch_variant_tuple(
                    western_pitch
                ),
                expected_pitch_variant_tuple,
            )

    def test_get_pitch_name_tuple_to_interval_quality_dict(self):
        for (
            pitch_variant_list_tuple,
            expected_pitch_name_tuple_to_interval_quality_dict,
        ) in (
            (
                # This 'pitch_variant_list_tuple' wouldn't exist
                # in reality, but it is still sufficient to test
                # the function
                (
                    [
                        (music_parameters.WesternPitch("c"),),
                        (music_parameters.WesternPitch("c", 5),),
                    ],
                    [
                        (
                            music_parameters.WesternPitch("g", 2),
                            music_parameters.WesternPitch("css"),
                        )
                    ],
                    [(music_parameters.WesternPitch("e"),)],
                ),
                {
                    ("c", "c"): False,
                    ("e", "e"): False,
                    ("g", "g"): False,
                    ("css", "css"): False,
                    ("c", "e"): False,
                    ("c", "g"): False,
                    ("c", "css"): True,
                    ("e", "g"): False,
                    ("css", "e"): True,
                    ("css", "g"): True,
                },
            ),
        ):
            self.assertEqual(
                music_converters.ImproveWesternPitchListSequenceReadability._get_pitch_name_tuple_to_interval_quality_dict(
                    pitch_variant_list_tuple
                ),
                expected_pitch_name_tuple_to_interval_quality_dict,
            )

    def test_get_search_space_and_real_search_space(self):
        for (
            pitch_variant_list_tuple,
            expected_search_space,
            expected_real_search_space,
        ) in (
            (
                (
                    [
                        (
                            music_parameters.WesternPitch("d"),
                            music_parameters.WesternPitch("css"),
                            music_parameters.WesternPitch("eff"),
                        ),
                        (
                            music_parameters.WesternPitch("g"),
                            music_parameters.WesternPitch("fss"),
                            music_parameters.WesternPitch("aff"),
                        ),
                    ],
                    [
                        (
                            music_parameters.WesternPitch("g"),
                            music_parameters.WesternPitch("fss"),
                        )
                    ],
                ),
                {"0_0": (0, 1, 2), "0_1": (0, 1, 2), "1_0": (0, 1)},
                {
                    "0_0": (
                        music_parameters.WesternPitch("d"),
                        music_parameters.WesternPitch("css"),
                        music_parameters.WesternPitch("eff"),
                    ),
                    "0_1": (
                        music_parameters.WesternPitch("g"),
                        music_parameters.WesternPitch("fss"),
                        music_parameters.WesternPitch("aff"),
                    ),
                    "1_0": (
                        music_parameters.WesternPitch("g"),
                        music_parameters.WesternPitch("fss"),
                    ),
                },
            ),
        ):
            self.assertEqual(
                music_converters.ImproveWesternPitchListSequenceReadability._get_search_space_and_real_search_space(
                    pitch_variant_list_tuple
                ),
                (expected_search_space, expected_real_search_space),
            )

    def test_convert_simple(self):
        self.assertEqual(
            self.improve_western_pitch_list_sequence_readability.convert(
                [
                    [
                        music_parameters.WesternPitch("c", octave=2),
                        music_parameters.WesternPitch("dss"),
                        music_parameters.WesternPitch("g"),
                    ]
                ]
            ),
            (
                [
                    music_parameters.WesternPitch("c", octave=2),
                    music_parameters.WesternPitch("e"),
                    music_parameters.WesternPitch("g"),
                ],
            ),
        )

    def test_convert_complex(self):
        self.assertEqual(
            self.improve_western_pitch_list_sequence_readability.convert(
                [
                    [
                        music_parameters.WesternPitch("c"),
                        music_parameters.WesternPitch("es", octave=3),
                    ],
                    [
                        music_parameters.WesternPitch("aff", octave=5),
                    ],
                    [
                        music_parameters.WesternPitch("ds"),
                    ],
                    [
                        music_parameters.WesternPitch("c"),
                        music_parameters.WesternPitch("gs"),
                    ],
                    [
                        music_parameters.WesternPitch("c"),
                    ],
                ]
            ),
            (
                [
                    music_parameters.WesternPitch("c"),
                    music_parameters.WesternPitch("f", octave=3),
                ],
                [
                    music_parameters.WesternPitch("g", octave=5),
                ],
                [
                    music_parameters.WesternPitch("ef"),
                ],
                [
                    music_parameters.WesternPitch("c"),
                    music_parameters.WesternPitch("af"),
                ],
                [
                    music_parameters.WesternPitch("c"),
                ],
            ),
        )


if __name__ == "__main__":
    unittest.main()
