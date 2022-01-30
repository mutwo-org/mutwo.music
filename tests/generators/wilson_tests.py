import unittest

from mutwo import music_generators
from mutwo import music_parameters


class CommonProductSetScaleTest(unittest.TestCase):
    def test_make_common_product_set_scale_with_one_number(self):
        self.assertEqual(
            music_generators.make_common_product_set_scale((3, 5, 7, 11), 1, True),
            tuple(
                music_parameters.JustIntonationPitch(ratio)
                for ratio in "3/1 5/1 7/1 11/1".split(" ")
            ),
        )

    def test_make_common_product_set_scale_with_two_numbers(self):
        self.assertEqual(
            music_generators.make_common_product_set_scale((3, 5, 7), 2, True),
            tuple(
                music_parameters.JustIntonationPitch(ratio)
                for ratio in "15/1 21/1 35/1".split(" ")
            ),
        )

    def test_make_common_product_set_scale_with_utonality(self):
        self.assertEqual(
            music_generators.make_common_product_set_scale((3, 5, 7), 2, False),
            tuple(
                music_parameters.JustIntonationPitch(ratio)
                for ratio in "1/15 1/21 1/35".split(" ")
            ),
        )

    def test_make_music_generatorss_brun_euclidean_algorithm_generator(self):
        pitch_tuple = (
            music_parameters.JustIntonationPitch("2/1"),
            music_parameters.JustIntonationPitch("3/2"),
            music_parameters.JustIntonationPitch("5/4"),
        )
        expected_interval_tuple_per_call_per_subtraction_index = (
            (
                (music_parameters.JustIntonationPitch("2/1"),),
                (
                    music_parameters.JustIntonationPitch("3/2"),
                    music_parameters.JustIntonationPitch("4/3"),
                ),
                (
                    music_parameters.JustIntonationPitch("4/3"),
                    music_parameters.JustIntonationPitch("9/8"),
                    music_parameters.JustIntonationPitch("4/3"),
                ),
                (
                    music_parameters.JustIntonationPitch("5/4"),
                    music_parameters.JustIntonationPitch("16/15"),
                    music_parameters.JustIntonationPitch("9/8"),
                    music_parameters.JustIntonationPitch("5/4"),
                    music_parameters.JustIntonationPitch("16/15"),
                ),
            ),
            (
                (music_parameters.JustIntonationPitch("2/1"),),
                (
                    music_parameters.JustIntonationPitch("5/4"),
                    music_parameters.JustIntonationPitch("8/5"),
                ),
                (
                    music_parameters.JustIntonationPitch("5/4"),
                    music_parameters.JustIntonationPitch("5/4"),
                    music_parameters.JustIntonationPitch("32/25"),
                ),
                (
                    music_parameters.JustIntonationPitch("5/4"),
                    music_parameters.JustIntonationPitch("5/4"),
                    music_parameters.JustIntonationPitch("6/5"),
                    music_parameters.JustIntonationPitch("16/15"),
                ),
            ),
        )
        for subtraction_index, expected_interval_tuple_per_call in zip(
            (1, 2), expected_interval_tuple_per_call_per_subtraction_index
        ):
            music_generatorss_brun_euclidean_algorithm_generator = (
                music_generators.make_wilsons_brun_euclidean_algorithm_generator(
                    pitch_tuple, subtraction_index
                )
            )
            for expected_interval_tuple in expected_interval_tuple_per_call:
                interval_tuple_tuple = next(music_generatorss_brun_euclidean_algorithm_generator)
                self.assertEqual((expected_interval_tuple,), interval_tuple_tuple)


if __name__ == "__main__":
    unittest.main()
