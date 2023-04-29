import unittest

from mutwo import music_parameters
from mutwo import music_utilities


class ScaleFamilyTest(unittest.TestCase):
    def test_init(self):
        scale_family = music_parameters.ScaleFamily(
            (
                music_parameters.WesternPitchInterval("p4"),
                music_parameters.WesternPitchInterval("m3"),
            )
        )
        self.assertTrue(scale_family)
        # Check if weight tuple as auto-assigned
        self.assertEqual(scale_family.weight_tuple, (1, 1))

        # Check if bad weight tuple raises error
        self.assertRaises(
            AssertionError,
            music_parameters.ScaleFamily,
            (music_parameters.WesternPitchInterval("p5"),),
            (1, 1),
        )

        # Check if unsorted interval tuple raises error
        self.assertRaises(
            music_utilities.UnsortedIntervalTupleError,
            music_parameters.ScaleFamily,
            (
                music_parameters.WesternPitchInterval("p5"),
                music_parameters.WesternPitchInterval("p1"),
                music_parameters.WesternPitchInterval("m3"),
            ),
        )

    def test_interval_tuple(self):
        for interval_tuple in (
            # Rising interval tuple
            (
                music_parameters.WesternPitchInterval("m3"),
                music_parameters.WesternPitchInterval("p4"),
            ),
            # Falling interval tuple
            (
                music_parameters.JustIntonationPitch("3/2"),
                music_parameters.JustIntonationPitch("4/3"),
            ),
        ):
            with self.subTest():
                self.assertEqual(
                    music_parameters.ScaleFamily(interval_tuple).interval_tuple,
                    interval_tuple,
                )

    def test_weight_tuple(self):
        self.assertEqual(
            music_parameters.ScaleFamily(
                (music_parameters.JustIntonationPitch(),), (0.33,)
            ).weight_tuple,
            (0.33,),
        )

    def test_is_rising_and_is_falling(self):
        for is_rising, is_falling, interval_tuple in (
            # Rising interval tuple
            (
                True,
                False,
                (
                    music_parameters.WesternPitchInterval("m3"),
                    music_parameters.WesternPitchInterval("p4"),
                ),
            ),
            # Falling interval tuple
            (
                False,
                True,
                (
                    music_parameters.JustIntonationPitch("3/2"),
                    music_parameters.JustIntonationPitch("4/3"),
                ),
            ),
        ):
            scale_family = music_parameters.ScaleFamily(interval_tuple)
            with self.subTest(interval_tuple=interval_tuple):
                self.assertEqual(scale_family.is_rising, is_rising)
                self.assertEqual(scale_family.is_falling, is_falling)

    def test_scale_degree_count(self):
        j = music_parameters.JustIntonationPitch
        scale_family = music_parameters.ScaleFamily(
            (j("1/1"), j("9/8"), j("5/4"), j("2/1"))
        )
        self.assertEqual(scale_family.scale_degree_count, 4)


class RepeatingScaleFamilyTest(unittest.TestCase):
    def setUp(self):
        self.repeating_interval_sequence = [
            music_parameters.JustIntonationPitch(ratio)
            for ratio in "1/1 9/8 5/4 3/2 7/4".split(" ")
        ]
        self.repeating_weight_sequence = (1, 2, 3, 4, 5)
        self.repeating_scale_family = music_parameters.RepeatingScaleFamily(
            self.repeating_interval_sequence,
            music_parameters.JustIntonationPitch("2/1"),
            min_pitch_interval=music_parameters.JustIntonationPitch("1/2"),
            max_pitch_interval=music_parameters.JustIntonationPitch("2/1"),
            repeating_weight_sequence=self.repeating_weight_sequence,
        )

    def test_init(self):
        # Minimal test to check if setUp works.
        self.assertTrue(self.repeating_scale_family)

    def test_interval_tuple(self):
        self.assertEqual(
            self.repeating_scale_family.interval_tuple,
            tuple(
                music_parameters.JustIntonationPitch(ratio)
                for ratio in ("1/2 9/16 5/8 3/4 7/8 1/1 9/8 5/4 3/2 7/4").split(" ")
            ),
        )

    def test_weight_tuple(self):
        self.assertEqual(
            self.repeating_scale_family.weight_tuple,
            (1, 2, 3, 4, 5, 1, 2, 3, 4, 5),
        )

    def test_scale_degree_tuple(self):
        self.assertEqual(
            self.repeating_scale_family.scale_degree_tuple,
            (0, 1, 2, 3, 4, 0, 1, 2, 3, 4),
        )

    def test_period_repetition_count_tuple(self):
        self.assertEqual(
            self.repeating_scale_family.period_repetition_count_tuple,
            (-1, -1, -1, -1, -1, 0, 0, 0, 0, 0),
        )

    def test_scale_degree_count(self):
        self.assertEqual(self.repeating_scale_family.scale_degree_count, 5)


class ScaleTest(unittest.TestCase):
    def _set_up_scale(self):
        scale_family = music_parameters.RepeatingScaleFamily(
            [
                music_parameters.JustIntonationPitch(ratio)
                for ratio in "1/1 9/8 5/4 3/2 7/4".split(" ")
            ],
            min_pitch_interval=music_parameters.JustIntonationPitch("1/1"),
            max_pitch_interval=music_parameters.JustIntonationPitch("4/1"),
        )
        scale = music_parameters.Scale(
            music_parameters.JustIntonationPitch("2/1"), scale_family
        )
        return scale, scale_family

    def setUp(self):
        self.scale, self.scale_family = self._set_up_scale()

    def test_pitch_tuple(self):
        self.assertEqual(
            self.scale.pitch_tuple,
            tuple(
                music_parameters.JustIntonationPitch(ratio)
                for ratio in "2/1 9/4 5/2 3/1 7/2 4/1 9/2 5/1 6/1 7/1".split(" ")
            ),
        )

    def test_tonic(self):
        self.assertEqual(self.scale.tonic, music_parameters.JustIntonationPitch("2/1"))

    def test_scale_family(self):
        self.assertEqual(self.scale.scale_family, self.scale_family)

    def test_scale_degree_tuple(self):
        self.assertEqual(
            self.scale.scale_degree_tuple,
            (0, 1, 2, 3, 4, 0, 1, 2, 3, 4),
        )

    def test_period_repetition_count_tuple(self):
        self.assertEqual(
            self.scale.period_repetition_count_tuple,
            (0, 0, 0, 0, 0, 1, 1, 1, 1, 1),
        )

    def test_scale_position_tuple(self):
        self.assertEqual(
            self.scale.scale_position_tuple,
            (
                (0, 0),
                (1, 0),
                (2, 0),
                (3, 0),
                (4, 0),
                (0, 1),
                (1, 1),
                (2, 1),
                (3, 1),
                (4, 1),
            ),
        )

    def test_set_tonic(self):
        self.scale.tonic = music_parameters.JustIntonationPitch("1/1")
        self.assertEqual(self.scale.pitch_tuple, self.scale.scale_family.interval_tuple)

    def test_equal(self):
        self.assertEqual(self.scale, self.scale)
        self.assertEqual(self.scale, self._set_up_scale()[0])
        self.assertNotEqual(self.scale, 100)

    def test_pitch_to_scale_index(self):
        self.assertEqual(
            self.scale.pitch_to_scale_index(
                music_parameters.JustIntonationPitch("2/1")
            ),
            0,
        )
        self.assertEqual(
            self.scale.pitch_to_scale_index(
                music_parameters.JustIntonationPitch("5/2")
            ),
            2,
        )

    def test_scale_index_to_pitch(self):
        self.assertEqual(
            self.scale.scale_index_to_pitch(0),
            music_parameters.JustIntonationPitch("2/1"),
        )
        self.assertEqual(
            self.scale.scale_index_to_pitch(2),
            music_parameters.JustIntonationPitch("5/2"),
        )

    def test_scale_position_to_pitch(self):
        self.assertEqual(
            self.scale.scale_position_to_pitch((0, 1)),
            music_parameters.JustIntonationPitch("4/1"),
        )
        self.assertEqual(
            self.scale.scale_position_to_pitch((0, 0)),
            music_parameters.JustIntonationPitch("2/1"),
        )
