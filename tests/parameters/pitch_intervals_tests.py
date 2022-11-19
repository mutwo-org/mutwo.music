import unittest

from mutwo import music_parameters


class DirectPitchIntervalTest(unittest.TestCase):
    def setUp(self):
        self.pitch_interval_0 = music_parameters.DirectPitchInterval(800)
        self.pitch_interval_1 = music_parameters.DirectPitchInterval(500)

    def test_interval(self):
        self.assertEqual(self.pitch_interval_0.interval, 800)
        self.assertEqual(self.pitch_interval_1.interval, 500)

    def test_set_interval(self):
        self.pitch_interval_0.interval = 100
        self.assertEqual(self.pitch_interval_0.interval, 100)

    def test_inverse(self):
        self.assertEqual(
            self.pitch_interval_1.inverse(), music_parameters.DirectPitchInterval(-500)
        )
        self.assertEqual(self.pitch_interval_0.inverse().interval, -800)


class WesternPitchIntervalTest(unittest.TestCase):
    def setUp(self):
        self.western_pitch_interval = music_parameters.WesternPitchInterval()

    def test_interval_type_to_interval_base_type(self):
        for interval_type, expected_interval_base_type in (
            ("1", "1"),
            ("7", "7"),
            ("8", "1"),
            ("9", "2"),
            ("15", "1"),
        ):
            self.assertEqual(
                music_parameters.WesternPitchInterval._interval_type_to_interval_base_type(
                    interval_type
                ),
                expected_interval_base_type,
            )

    def test_interval_type_to_octave_count(self):
        for interval_type, expected_octave_count in (
            ("1", 0),
            ("7", 0),
            ("8", 1),
            ("9", 1),
            ("15", 2),
        ):
            self.assertEqual(
                music_parameters.WesternPitchInterval._interval_type_to_octave_count(
                    interval_type
                ),
                expected_octave_count,
            )

    def test_is_interval_type_perfect(self):
        for interval_type, is_interval_type_perfect in (
            ("1", True),
            ("7", False),
            ("8", True),
            ("9", False),
            ("10", False),
            ("15", True),
        ):
            self.assertEqual(
                music_parameters.WesternPitchInterval.is_interval_type_perfect(
                    interval_type
                ),
                is_interval_type_perfect,
            )

    def test_is_interval_type_imperfect(self):
        for interval_type, is_interval_type_imperfect in (
            ("1", False),
            ("7", True),
            ("8", False),
            ("9", True),
            ("10", True),
            ("15", False),
        ):
            self.assertEqual(
                music_parameters.WesternPitchInterval.is_interval_type_imperfect(
                    interval_type
                ),
                is_interval_type_imperfect,
            )

    def test_semitone_count_to_interval_data(self):
        for semitone_count, expected_interval_data in (
            (0, ("1", "p", False)),
            (1, ("2", "m", False)),
            (2, ("2", "M", False)),
            (3, ("3", "m", False)),
            (4, ("3", "M", False)),
            (5, ("4", "p", False)),
            (7, ("5", "p", False)),
            (8, ("6", "m", False)),
            (9, ("6", "M", False)),
            (10, ("7", "m", False)),
            (11, ("7", "M", False)),
            (12, ("8", "p", False)),
            (13, ("9", "m", False)),
            (-1, ("2", "m", True)),
            (-2, ("2", "M", True)),
            (-3, ("3", "m", True)),
            (-12, ("8", "p", True)),
        ):
            self.assertEqual(
                music_parameters.WesternPitchInterval._semitone_count_to_interval_data(
                    semitone_count
                ),
                expected_interval_data,
            )

    def test_interval_type_base_type(self):
        for interval_name, expected_interval_base_type in (
            ("m3", "3"),
            ("p8", "1"),
            ("p4", "4"),
            ("dd11", "4"),
            ("AA4", "4"),
            ("m-6", "6"),
        ):
            self.assertEqual(
                music_parameters.WesternPitchInterval(
                    interval_name
                ).interval_type_base_type,
                expected_interval_base_type,
            )

    def test_interval_name_to_interval_data(self):
        for interval_name, expected_interval_data in (
            ("p4", ("4", "p", False)),
            ("ddd4", ("4", "ddd", False)),
            ("M7", ("7", "M", False)),
            ("m7", ("7", "m", False)),
            ("p-8", ("8", "p", True)),
            ("AA-11", ("11", "AA", True)),
        ):
            self.assertEqual(
                music_parameters.WesternPitchInterval._interval_name_to_interval_data(
                    interval_name
                ),
                expected_interval_data,
            )

    def test_assert_interval_quality_avoids_illegal_stacking(self):
        self.assertRaises(
            Exception,
            lambda: music_parameters.WesternPitchInterval._assert_interval_quality_avoids_illegal_stacking(
                [
                    music_parameters.constants.WESTERN_PITCH_INTERVAL_QUALITY_MAJOR,
                    music_parameters.constants.WESTERN_PITCH_INTERVAL_QUALITY_MAJOR,
                ]
            ),
        )
        self.assertEqual(
            music_parameters.WesternPitchInterval._assert_interval_quality_avoids_illegal_stacking(
                [
                    music_parameters.constants.WESTERN_PITCH_INTERVAL_QUALITY_DIMINISHED,
                    music_parameters.constants.WESTERN_PITCH_INTERVAL_QUALITY_DIMINISHED,
                ]
            ),
            None,
        )

    def test_assert_interval_quality_is_not_mixed(self):
        self.assertRaises(
            Exception,
            lambda: music_parameters.WesternPitchInterval._assert_interval_quality_avoids_illegal_stacking(
                [
                    music_parameters.constants.WESTERN_PITCH_INTERVAL_QUALITY_MINOR,
                    music_parameters.constants.WESTERN_PITCH_INTERVAL_QUALITY_DIMINISHED,
                    music_parameters.constants.WESTERN_PITCH_INTERVAL_QUALITY_MAJOR,
                ]
            ),
        )

    def test_assert_interval_quality_fits_to_interval_type(self):
        self.assertRaises(
            Exception,
            lambda: music_parameters.WesternPitchInterval._assert_interval_quality_fits_to_interval_type(
                "p", "2"
            ),
        )
        self.assertRaises(
            Exception,
            lambda: music_parameters.WesternPitchInterval._assert_interval_quality_fits_to_interval_type(
                "m", "5"
            ),
        )

    def test_initialisation_by_interval_name(self):
        western_pitch_interval0 = music_parameters.WesternPitchInterval("p4")
        self.assertEqual(western_pitch_interval0.interval_type, "4")
        self.assertEqual(western_pitch_interval0.interval_quality, "p")
        self.assertEqual(western_pitch_interval0.is_interval_falling, False)

        western_pitch_interval1 = music_parameters.WesternPitchInterval("p-4")
        self.assertEqual(western_pitch_interval1.interval_type, "4")
        self.assertEqual(western_pitch_interval1.interval_quality, "p")
        self.assertEqual(western_pitch_interval1.is_interval_falling, True)

        western_pitch_interval2 = music_parameters.WesternPitchInterval("dd8")
        self.assertEqual(western_pitch_interval2.interval_type, "8")
        self.assertEqual(western_pitch_interval2.interval_quality, "dd")
        self.assertEqual(western_pitch_interval2.is_interval_falling, False)

    def test_initialisation_by_semitone_count(self):
        western_pitch_interval0 = music_parameters.WesternPitchInterval(0)
        self.assertEqual(western_pitch_interval0.interval_type, "1")
        self.assertEqual(western_pitch_interval0.interval_quality, "p")
        self.assertEqual(western_pitch_interval0.is_interval_falling, False)
        self.assertEqual(western_pitch_interval0.semitone_count, 0)

        western_pitch_interval1 = music_parameters.WesternPitchInterval(-12)
        self.assertEqual(western_pitch_interval1.interval_type, "8")
        self.assertEqual(western_pitch_interval1.interval_quality, "p")
        self.assertEqual(western_pitch_interval1.is_interval_falling, True)
        self.assertEqual(western_pitch_interval1.semitone_count, -12)

    def test_raise_invalid_interval_quality_error(self):
        self.assertRaises(
            NameError,
            lambda: self.western_pitch_interval._raise_invalid_interval_quality_error(
                "X", "XXXX"
            ),
        )

    def test_interval_quality_string_to_interval_quality_tuple(self):
        for interval_quality_string, expected_interval_quality_tuple in (
            ("p", (music_parameters.constants.WESTERN_PITCH_INTERVAL_QUALITY_PERFECT,)),
            ("M", (music_parameters.constants.WESTERN_PITCH_INTERVAL_QUALITY_MAJOR,)),
            ("m", (music_parameters.constants.WESTERN_PITCH_INTERVAL_QUALITY_MINOR,)),
            (
                "A",
                (music_parameters.constants.WESTERN_PITCH_INTERVAL_QUALITY_AUGMENTED,),
            ),
            (
                "dd",
                (
                    music_parameters.constants.WESTERN_PITCH_INTERVAL_QUALITY_DIMINISHED,
                    music_parameters.constants.WESTERN_PITCH_INTERVAL_QUALITY_DIMINISHED,
                ),
            ),
        ):
            self.assertEqual(
                self.western_pitch_interval._interval_quality_string_to_interval_quality_tuple(
                    interval_quality_string
                ),
                expected_interval_quality_tuple,
            )

    def test_raise_error_if_interval_quality_and_interval_type_do_not_fit(self):
        self.assertRaises(
            Exception,
            lambda: self.western_pitch_interval._raise_error_if_interval_quality_and_interval_type_do_not_fit(
                "p", "2"
            ),
        )
        self.assertEqual(
            self.western_pitch_interval._raise_error_if_interval_quality_and_interval_type_do_not_fit(
                "p", "1"
            ),
            None,
        )

    def test_raise_error_if_interval_quality_is_invalid(self):
        self.assertRaises(
            NameError,
            lambda: self.western_pitch_interval._raise_error_if_interval_quality_is_invalid(
                "X"
            ),
        )
        self.assertRaises(
            Exception,
            lambda: self.western_pitch_interval._raise_error_if_interval_quality_is_invalid(
                "mM"
            ),
        )
        self.assertRaises(
            Exception,
            lambda: self.western_pitch_interval._raise_error_if_interval_quality_is_invalid(
                "mmm"
            ),
        )

    def test_raise_error_if_interval_type_is_invalid(self):
        self.assertRaises(
            Exception,
            lambda: self.western_pitch_interval._raise_error_if_interval_type_is_invalid(
                "0"
            ),
        )
        self.assertRaises(
            Exception,
            lambda: self.western_pitch_interval._raise_error_if_interval_type_is_invalid(
                "hello"
            ),
        )

    def test_is_interval_rising(self):
        self.assertEqual(
            music_parameters.WesternPitchInterval(2).is_interval_rising, True
        )
        self.assertEqual(
            music_parameters.WesternPitchInterval(-10).is_interval_rising, False
        )

    def test_set_is_interval_rising(self):
        western_pitch_interval = music_parameters.WesternPitchInterval(2)
        western_pitch_interval.is_interval_rising = False
        self.assertEqual(western_pitch_interval.is_interval_rising, False)
        self.assertEqual(western_pitch_interval.semitone_count, -2)

    def test_interval_quality_tuple(self):
        self.assertEqual(
            music_parameters.WesternPitchInterval("p8").interval_quality_tuple,
            (music_parameters.constants.WESTERN_PITCH_INTERVAL_QUALITY_PERFECT,),
        )

    def test_interval_type_cent_deviation(self):
        for pitch_interval_name, expected_cent_deviation in (
            ("p8", 1200),
            ("m-6", 900),
            ("dd4", 500),
            ("p15", 2400),
        ):
            self.assertEqual(
                music_parameters.WesternPitchInterval(
                    pitch_interval_name
                ).interval_type_cent_deviation,
                expected_cent_deviation,
            )

    def test_interval_quality_cent_deviation(self):
        for pitch_interval_name, expected_cent_deviation in (
            ("p8", 0),
            ("m-6", -100),
            ("dd4", -200),
            ("dd3", -300),
            ("A11", 100),
            ("AAAAA15", 500),
            ("M2", 0),
        ):
            self.assertEqual(
                music_parameters.WesternPitchInterval(
                    pitch_interval_name
                ).interval_quality_cent_deviation,
                expected_cent_deviation,
            )

    def test_name(self):
        for interval_name in ("p-8", "dddd15", "A321", "AAA-15"):
            self.assertEqual(
                music_parameters.WesternPitchInterval(interval_name).name, interval_name
            )

    def test_is_perfect_interval(self):
        for interval_name, is_perfect_interval in (("p-8", True), ("m2", False)):
            self.assertEqual(
                music_parameters.WesternPitchInterval(
                    interval_name
                ).is_perfect_interval,
                is_perfect_interval,
            )

    def test_is_imperfect_interval(self):
        for interval_name, is_imperfect_interval in (("p-8", False), ("m2", True)):
            self.assertEqual(
                music_parameters.WesternPitchInterval(
                    interval_name
                ).is_imperfect_interval,
                is_imperfect_interval,
            )

    def test_interval(self):
        for interval_name_or_semitone_count, expected_interval in (
            (13, 1300),
            (14.3, 1400),
            ("d-2", 0),
            ("p-15", -2400),
            ("AA8", 1400),
        ):
            self.assertEqual(
                music_parameters.WesternPitchInterval(
                    interval_name_or_semitone_count
                ).interval,
                expected_interval,
            )

    def test_semitone_count(self):
        for interval_name_or_semitone_count, expected_semitone_count in ((100, 100),):
            self.assertEqual(
                music_parameters.WesternPitchInterval(
                    interval_name_or_semitone_count
                ).semitone_count,
                expected_semitone_count,
            )

    def test_diatonic_pitch_class_count(self):
        for interval_name_or_semitone_count, expected_diatonic_pitch_class_count in (
            (-1, -1),
            ("m3", 2),
            ("ddd4", 3),
            ("M-2", -1),
        ):
            self.assertEqual(
                music_parameters.WesternPitchInterval(
                    interval_name_or_semitone_count
                ).diatonic_pitch_class_count,
                expected_diatonic_pitch_class_count,
            )

    def test_can_be_simplified(self):
        for interval_name, can_be_simplified in (
            ("m3", False),
            ("M-6", False),
            ("A8", True),
            ("A4", False),
            ("d5", False),
            ("dd5", True),
            ("p1", False),
            ("m9", False),
            ("d13", True),
        ):
            self.assertEqual(
                music_parameters.WesternPitchInterval(interval_name).can_be_simplified,
                can_be_simplified,
            )

    def test_inverse(self):
        self.assertEqual(
            music_parameters.WesternPitchInterval("m3").inverse(),
            music_parameters.WesternPitchInterval("m-3"),
        )
        self.assertEqual(
            music_parameters.WesternPitchInterval("p-11").inverse(),
            music_parameters.WesternPitchInterval("p11"),
        )


if __name__ == "__name__":
    unittest.main()
