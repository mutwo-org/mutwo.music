import unittest


try:
    import quicktions as fractions  # type: ignore
except ImportError:
    import fractions  # type: ignore

from mutwo import core_utilities
from mutwo import music_parameters


class Partial_Test(unittest.TestCase):
    def setUp(self):
        self.partial = music_parameters.Partial(3)
        self.negative_partial = music_parameters.Partial(5, tonality=False)

    def test_index(self):
        self.assertEqual(self.partial.index, 3)
        self.assertEqual(self.negative_partial.index, 5)

    def test_interval(self):
        self.assertEqual(
            self.partial.interval, music_parameters.JustIntonationPitch("3/1")
        )
        self.assertEqual(
            self.negative_partial.interval, music_parameters.JustIntonationPitch("1/5")
        )


class DirectPitch_Test(unittest.TestCase):
    def test_property_frequency(self):
        frequency0 = 200
        frequency1 = 502.42
        frequency2 = 10
        self.assertEqual(frequency0, music_parameters.DirectPitch(frequency0).frequency)
        self.assertEqual(frequency1, music_parameters.DirectPitch(frequency1).frequency)
        self.assertEqual(frequency2, music_parameters.DirectPitch(frequency2).frequency)

    def test_get_pitch_interval(self):
        pitch0 = music_parameters.DirectPitch(200)
        pitch1 = music_parameters.DirectPitch(400)
        self.assertEqual(
            pitch0.get_pitch_interval(pitch1),
            music_parameters.DirectPitchInterval(1200),
        )
        self.assertEqual(
            pitch1.get_pitch_interval(pitch0),
            music_parameters.DirectPitchInterval(-1200),
        )


class MidiPitch_Test(unittest.TestCase):
    def test_property_frequency(self):
        frequency0 = 440
        frequency1 = 261.626
        self.assertEqual(frequency0, music_parameters.MidiPitch(69).frequency)
        self.assertEqual(frequency1, round(music_parameters.MidiPitch(60).frequency, 3))


class EqualDividedOctavePitch_Test(unittest.TestCase):
    def test_false_pitch_class(self):
        self.assertRaises(
            ValueError,
            lambda: music_parameters.EqualDividedOctavePitch(12, -2, 0, 0, 0),
        )
        self.assertRaises(
            ValueError,
            lambda: music_parameters.EqualDividedOctavePitch(12, 13, 0, 0, 0),
        )

    def test_property_frequency(self):
        pitch0 = music_parameters.EqualDividedOctavePitch(12, 0, 1, 0, 0)
        pitch1 = music_parameters.EqualDividedOctavePitch(6, 0, -1, 0, 0)
        pitch2 = music_parameters.EqualDividedOctavePitch(12, 6, 0, 0, 0)
        self.assertAlmostEqual(pitch0.frequency, pitch0.concert_pitch.frequency * 2)
        self.assertAlmostEqual(pitch1.frequency, pitch1.concert_pitch.frequency * 0.5)
        self.assertAlmostEqual(pitch2.frequency, 622.254)

    def test_property_step_factor(self):
        pitch0 = music_parameters.EqualDividedOctavePitch(12, 0, 1, 0, 0)
        pitch1 = music_parameters.EqualDividedOctavePitch(6, 0, -1, 0, 0)
        self.assertAlmostEqual(
            (pitch0.step_factor**pitch0.n_pitch_classes_per_octave)
            * pitch0.concert_pitch.frequency,
            pitch0.frequency,
        )
        self.assertAlmostEqual(
            pitch1.concert_pitch.frequency
            / (pitch1.step_factor**pitch1.n_pitch_classes_per_octave),
            pitch1.frequency,
        )

    def test_magic_method_sub(self):
        pitch0 = music_parameters.EqualDividedOctavePitch(12, 7, 0, 0, 0)
        pitch1 = music_parameters.EqualDividedOctavePitch(12, 1, 0, 0, 0)
        pitch2 = music_parameters.EqualDividedOctavePitch(12, 0, 1, 0, 0)
        pitch3 = music_parameters.EqualDividedOctavePitch(24, 1, 0, 0, 0)
        self.assertEqual(pitch0 - pitch1, 6)
        self.assertEqual(pitch2 - pitch0, 5)
        self.assertEqual(pitch2 - pitch1, 11)
        self.assertRaises(ValueError, lambda: pitch3 - pitch1)

    def test_add(self):
        pitch0 = music_parameters.EqualDividedOctavePitch(12, 7, 0, 0, 0)
        pitch1 = music_parameters.EqualDividedOctavePitch(12, 1, 0, 0, 0)
        pitch2 = music_parameters.EqualDividedOctavePitch(12, 0, 1, 0, 0)
        pitch3 = music_parameters.EqualDividedOctavePitch(12, 11, -1, 0, 0)
        pitch4 = music_parameters.EqualDividedOctavePitch(12, 0, 0, 0, 0)
        pitch4.add(-1)
        self.assertEqual(pitch0.add(-6, mutate=False), pitch1)
        self.assertEqual(pitch0.add(5, mutate=False), pitch2)
        self.assertEqual(pitch0.add(-8, mutate=False), pitch3)
        self.assertEqual(pitch4, pitch3)

    def test_subtract(self):
        pitch0 = music_parameters.EqualDividedOctavePitch(12, 7, 0, 0, 0)
        pitch1 = music_parameters.EqualDividedOctavePitch(12, 1, 0, 0, 0)
        pitch2 = music_parameters.EqualDividedOctavePitch(12, 0, 1, 0, 0)
        pitch3 = music_parameters.EqualDividedOctavePitch(12, 11, -1, 0, 0)
        pitch4 = music_parameters.EqualDividedOctavePitch(12, 0, 0, 0, 0)
        pitch4.subtract(1)
        self.assertEqual(pitch0.subtract(6, mutate=False), pitch1)
        self.assertEqual(pitch0.subtract(-5, mutate=False), pitch2)
        self.assertEqual(pitch0.subtract(8, mutate=False), pitch3)
        self.assertEqual(pitch4, pitch3)


class WesternPitchTest(unittest.TestCase):
    def test_constructor_from_string(self):
        pitch0 = music_parameters.WesternPitch("cf", 4)
        pitch1 = music_parameters.WesternPitch("dqs", 3)
        pitch2 = music_parameters.WesternPitch("gss")
        pitch3 = music_parameters.WesternPitch("ges", 0)
        pitch4 = music_parameters.WesternPitch("bss", 10)
        self.assertEqual(pitch0.name, "cf4")
        self.assertEqual(pitch1.name, "dqs3")
        self.assertEqual(pitch2.name, "gss4")
        self.assertEqual(pitch3.name, "ges0")
        self.assertEqual(pitch4.name, "bss10")
        self.assertEqual(pitch0.pitch_class, -1)
        self.assertEqual(pitch1.pitch_class, 2.5)
        self.assertEqual(pitch2.pitch_class, 9)
        self.assertEqual(pitch3.pitch_class, 7.25)
        self.assertEqual(pitch4.pitch_class, 13)

    def test_constructor_from_float(self):
        pitch0 = music_parameters.WesternPitch(0)
        pitch1 = music_parameters.WesternPitch(1)
        pitch2 = music_parameters.WesternPitch(2.25)
        pitch3 = music_parameters.WesternPitch(-0.5)
        pitch4 = music_parameters.WesternPitch(7.166, 5)
        self.assertEqual(pitch0.name, "c4")
        self.assertEqual(pitch1.name, "df4")
        self.assertEqual(pitch2.name, "des4")
        self.assertEqual(pitch3.name, "cqf4")
        self.assertEqual(pitch4.name, "gts5")

    def test_representation(self):
        self.assertEqual(
            repr(music_parameters.WesternPitch("cs", 2)), "WesternPitch('cs', 2)"
        )

    def test_property_frequency(self):
        pitch0 = music_parameters.WesternPitch("a", 4)
        pitch1 = music_parameters.WesternPitch("a", 3)
        pitch2 = music_parameters.WesternPitch("a", 5)
        pitch3 = music_parameters.WesternPitch("as", 4)
        pitch4 = music_parameters.WesternPitch("bqs", 4)
        self.assertAlmostEqual(
            pitch0.frequency, music_parameters.configurations.DEFAULT_CONCERT_PITCH
        )
        self.assertAlmostEqual(
            pitch1.frequency,
            music_parameters.configurations.DEFAULT_CONCERT_PITCH * 0.5,
        )
        self.assertAlmostEqual(
            pitch2.frequency, music_parameters.configurations.DEFAULT_CONCERT_PITCH * 2
        )
        self.assertAlmostEqual(
            pitch3.frequency,
            core_utilities.round_floats(
                music_parameters.configurations.DEFAULT_CONCERT_PITCH
                * pitch3.step_factor,
                music_parameters.configurations.EQUAL_DIVIDED_OCTAVE_PITCH_ROUND_FREQUENCY_DIGIT_COUNT,
            ),
        )
        self.assertAlmostEqual(
            pitch4.frequency,
            core_utilities.round_floats(
                music_parameters.configurations.DEFAULT_CONCERT_PITCH
                * (pitch4.step_factor**2.5),
                music_parameters.configurations.EQUAL_DIVIDED_OCTAVE_PITCH_ROUND_FREQUENCY_DIGIT_COUNT,
            ),
        )

    def test_property_diatonic_pitch_class_name(self):
        self.assertEqual(
            music_parameters.WesternPitch("cs").diatonic_pitch_class_name, "c"
        )
        self.assertEqual(
            music_parameters.WesternPitch("a").diatonic_pitch_class_name, "a"
        )

    def test_property_accidental_name(self):
        self.assertEqual(music_parameters.WesternPitch("cs").accidental_name, "s")
        self.assertEqual(music_parameters.WesternPitch("a").accidental_name, "")
        self.assertEqual(music_parameters.WesternPitch("fff").accidental_name, "ff")

    def test_property_is_microtonal(self):
        for pitch_name, is_microtonal in (
            ("c", False),
            ("cs", False),
            ("ess", False),
            ("aqf", True),
            ("dxs", True),
        ):
            self.assertEqual(
                music_parameters.WesternPitch(pitch_name).is_microtonal, is_microtonal
            )

    def test_property_enharmonic_pitch_tuple(self):
        for pitch_name, expected_enharmonic_pitch_tuple in (
            (
                "c",
                (
                    music_parameters.WesternPitch("bs", octave=3),
                    music_parameters.WesternPitch("dff"),
                ),
            ),
            (
                "ds",
                (music_parameters.WesternPitch("ef"),),
            ),
            (
                "a",
                (
                    music_parameters.WesternPitch("gss"),
                    music_parameters.WesternPitch("bff"),
                ),
            ),
            (
                "bs",
                (music_parameters.WesternPitch("c", octave=5),),
            ),
            (
                "gss",
                (music_parameters.WesternPitch("a"),),
            ),
            (
                "ff",
                (music_parameters.WesternPitch("e"),),
            ),
        ):
            self.assertEqual(
                music_parameters.WesternPitch(pitch_name).enharmonic_pitch_tuple,
                expected_enharmonic_pitch_tuple,
            )

    def test_add_western_pitch_interval(self):
        for western_pitch_name, western_pitch_interval_name, expected_western_pitch in (
            ("c", "p1", music_parameters.WesternPitch("c")),
            ("cqs", "M2", music_parameters.WesternPitch("dqs")),
            ("f", "p4", music_parameters.WesternPitch("bf")),
            ("c", "m3", music_parameters.WesternPitch("ef")),
            ("c", "m-9", music_parameters.WesternPitch("b", octave=2)),
            ("d", "M3", music_parameters.WesternPitch("fs")),
            ("c", "p8", music_parameters.WesternPitch("c", octave=5)),
            ("c", "m-3", music_parameters.WesternPitch("a", octave=3)),
        ):
            self.assertEqual(
                music_parameters.WesternPitch(western_pitch_name).add(
                    music_parameters.WesternPitchInterval(western_pitch_interval_name)
                ),
                expected_western_pitch,
            )

    def test_subtract_western_pitch_interval(self):
        for western_pitch_name, western_pitch_interval_name, expected_western_pitch in (
            ("c", "p1", music_parameters.WesternPitch("c")),
            ("f", "p4", music_parameters.WesternPitch("c")),
            ("c", "m3", music_parameters.WesternPitch("a", octave=3)),
            ("c", "m-9", music_parameters.WesternPitch("df", octave=5)),
            ("d", "m3", music_parameters.WesternPitch("b", octave=3)),
            ("d", "M3", music_parameters.WesternPitch("bf", octave=3)),
            ("c", "p8", music_parameters.WesternPitch("c", octave=3)),
            ("c", "m-3", music_parameters.WesternPitch("ef")),
        ):
            self.assertEqual(
                music_parameters.WesternPitch(western_pitch_name).subtract(
                    music_parameters.WesternPitchInterval(western_pitch_interval_name)
                ),
                expected_western_pitch,
            )

    def test_add_western_pitch_interval_name(self):
        self.assertEqual(
            music_parameters.WesternPitch("e").add("A3"),
            music_parameters.WesternPitch("gss"),
        )

    def test_subtract_western_pitch_interval_name(self):
        self.assertEqual(
            music_parameters.WesternPitch("a").subtract("d6"),
            music_parameters.WesternPitch("css"),
        )

    def test_add_semitone_count(self):
        self.assertEqual(
            music_parameters.WesternPitch("d").add(4),
            music_parameters.WesternPitch("fs"),
        )

    def test_subtract_semitone_count(self):
        self.assertEqual(
            music_parameters.WesternPitch("a").subtract(8),
            music_parameters.WesternPitch("cs"),
        )

    def test_base_interval_type_and_interval_quality_semitone_count_to_interval_quality(
        self,
    ):
        for (
            base_interval_type,
            interval_quality_semitone_count,
            expected_interval_quality,
        ) in (
            ("5", 0, "p"),
            ("4", 2, "AA"),
            ("1", -1, "d"),
            ("2", 0, "M"),
            ("7", -1, "m"),
            ("6", 1, "A"),
            ("6", -3, "dd"),
        ):
            self.assertEqual(
                music_parameters.WesternPitch._base_interval_type_and_interval_quality_semitone_count_to_interval_quality(
                    base_interval_type, interval_quality_semitone_count
                ),
                expected_interval_quality,
            )

    def test_get_pitch_interval(self):
        for pitch0, pitch1, expected_pitch_interval in (
            (
                music_parameters.WesternPitch("c"),
                music_parameters.WesternPitch("f"),
                music_parameters.WesternPitchInterval("p4"),
            ),
            (
                music_parameters.WesternPitch("c"),
                music_parameters.WesternPitch("f", octave=3),
                music_parameters.WesternPitchInterval("p-5"),
            ),
            (
                music_parameters.WesternPitch("d"),
                music_parameters.WesternPitch("a"),
                music_parameters.WesternPitchInterval("p5"),
            ),
            (
                music_parameters.WesternPitch("c"),
                music_parameters.WesternPitch("es"),
                music_parameters.WesternPitchInterval("A3"),
            ),
            (
                music_parameters.WesternPitch("d"),
                music_parameters.WesternPitch("bss"),
                music_parameters.WesternPitchInterval("AA6"),
            ),
            (
                music_parameters.WesternPitch("c"),
                music_parameters.WesternPitch("c", octave=5),
                music_parameters.WesternPitchInterval("p8"),
            ),
            (
                music_parameters.WesternPitch("b"),
                music_parameters.WesternPitch("f", octave=5),
                music_parameters.WesternPitchInterval("d5"),
            ),
            (
                music_parameters.WesternPitch("d"),
                music_parameters.WesternPitch("f"),
                music_parameters.WesternPitchInterval("m3"),
            ),
            (
                music_parameters.WesternPitch("f"),
                music_parameters.WesternPitch("d"),
                music_parameters.WesternPitchInterval("m-3"),
            ),
            (
                music_parameters.WesternPitch("df"),
                music_parameters.WesternPitch("f"),
                music_parameters.WesternPitchInterval("M3"),
            ),
            (
                music_parameters.WesternPitch("f"),
                music_parameters.WesternPitch("df"),
                music_parameters.WesternPitchInterval("M-3"),
            ),
        ):
            self.assertEqual(pitch0.get_pitch_interval(pitch1), expected_pitch_interval)

    def test_round_to(self):
        w = music_parameters.WesternPitch
        for w0, w1 in (
            (w("cqs", 5), w("cs", 5)),
            (w("fets", 2), w("fss", 2)),
            (w("df", 7), w("df", 7)),
            (w("a", 1), w("a", 1)),
            (w("brf", 2), w("bf", 2)),
        ):
            self.assertEqual(w0.round_to(), w1)

        self.assertEqual(
            w("cqs").round_to((fractions.Fraction(1, 1), fractions.Fraction(1, 2))),
            w("cqs"),
        )


class JustIntonationPitchTest(unittest.TestCase):
    def test_constructor_from_string(self):
        self.assertEqual(
            music_parameters.JustIntonationPitch("3/2").ratio, fractions.Fraction(3, 2)
        )
        self.assertEqual(
            music_parameters.JustIntonationPitch("5/1").ratio, fractions.Fraction(5, 1)
        )
        self.assertEqual(
            music_parameters.JustIntonationPitch("1/17").ratio,
            fractions.Fraction(1, 17),
        )

    def test_get_pitch_interval(self):
        pitch0 = music_parameters.JustIntonationPitch("1/1")
        pitch1 = music_parameters.JustIntonationPitch("2/1")
        pitch2 = music_parameters.DirectPitch(
            music_parameters.configurations.DEFAULT_CONCERT_PITCH
        )
        pitch3 = music_parameters.DirectPitch(
            music_parameters.configurations.DEFAULT_CONCERT_PITCH * 2
        )
        self.assertEqual(pitch0.get_pitch_interval(pitch1), pitch1)
        self.assertEqual(
            pitch1.get_pitch_interval(pitch0), pitch1.inverse(mutate=False)
        )
        self.assertEqual(
            pitch0.get_pitch_interval(pitch2), music_parameters.DirectPitchInterval(0)
        )
        self.assertEqual(
            pitch0.get_pitch_interval(pitch3),
            music_parameters.DirectPitchInterval(1200),
        )
        self.assertEqual(
            pitch3.get_pitch_interval(pitch0),
            music_parameters.DirectPitchInterval(-1200),
        )

    def test_constructor_from_ratio(self):
        ratio0 = fractions.Fraction(3, 2)
        ratio1 = fractions.Fraction(5, 1)
        ratio2 = fractions.Fraction(1, 17)
        self.assertEqual(music_parameters.JustIntonationPitch(ratio0).ratio, ratio0)
        self.assertEqual(music_parameters.JustIntonationPitch(ratio1).ratio, ratio1)
        self.assertEqual(music_parameters.JustIntonationPitch(ratio2).ratio, ratio2)

    def test_constructor_from_vector(self):
        ratio0 = fractions.Fraction(3, 2)
        ratio1 = fractions.Fraction(5, 1)
        ratio2 = fractions.Fraction(1, 17)
        self.assertEqual(music_parameters.JustIntonationPitch((-1, 1)).ratio, ratio0)
        self.assertEqual(music_parameters.JustIntonationPitch((0, 0, 1)).ratio, ratio1)
        self.assertEqual(
            music_parameters.JustIntonationPitch([0, 0, 0, 0, 0, 0, -1]).ratio, ratio2
        )

    def test_constructor_with_different_concert_pitch(self):
        concert_pitch0 = music_parameters.DirectPitch(300)
        concert_pitch1 = music_parameters.DirectPitch(200)
        self.assertEqual(
            music_parameters.JustIntonationPitch(
                concert_pitch=concert_pitch0
            ).concert_pitch,
            concert_pitch0,
        )
        self.assertEqual(
            music_parameters.JustIntonationPitch(
                concert_pitch=concert_pitch1.frequency
            ).concert_pitch,
            concert_pitch1,
        )

    def test_compare_with_other_pitch(self):
        p0 = music_parameters.JustIntonationPitch("3/2")
        p1 = music_parameters.DirectPitch(100)
        self.assertGreater(p0, p1)
        self.assertLess(p1, p0)

    def test_property_exponent_tuple(self):
        ratio0 = fractions.Fraction(3, 2)
        ratio1 = fractions.Fraction(25, 1)
        ratio2 = fractions.Fraction(11, 9)
        self.assertEqual(
            music_parameters.JustIntonationPitch(ratio0).exponent_tuple, (-1, 1)
        )
        self.assertEqual(
            music_parameters.JustIntonationPitch(ratio1).exponent_tuple, (0, 0, 2)
        )
        self.assertEqual(
            music_parameters.JustIntonationPitch(ratio2).exponent_tuple,
            (0, -2, 0, 0, 1),
        )

    def test_property_prime_tuple(self):
        ratio0 = fractions.Fraction(3, 2)
        ratio1 = fractions.Fraction(25, 1)
        ratio2 = fractions.Fraction(11, 9)
        self.assertEqual(
            music_parameters.JustIntonationPitch(ratio0).prime_tuple, (2, 3)
        )
        self.assertEqual(
            music_parameters.JustIntonationPitch(ratio1).prime_tuple, (2, 3, 5)
        )
        self.assertEqual(
            music_parameters.JustIntonationPitch(ratio2).prime_tuple, (2, 3, 5, 7, 11)
        )

    def test_property_occupied_primes(self):
        ratio0 = fractions.Fraction(3, 2)
        ratio1 = fractions.Fraction(25, 1)
        ratio2 = fractions.Fraction(11, 9)
        self.assertEqual(
            music_parameters.JustIntonationPitch(ratio0).occupied_primes, (2, 3)
        )
        self.assertEqual(
            music_parameters.JustIntonationPitch(ratio1).occupied_primes, (5,)
        )
        self.assertEqual(
            music_parameters.JustIntonationPitch(ratio2).occupied_primes, (3, 11)
        )

    def test_property_frequency(self):
        ratio0 = fractions.Fraction(3, 2)
        concert_pitch0 = 200
        ratio1 = fractions.Fraction(25, 1)
        concert_pitch1 = 300
        ratio2 = fractions.Fraction(11, 9)
        concert_pitch2 = 10
        self.assertAlmostEqual(
            music_parameters.JustIntonationPitch(ratio0, concert_pitch0).frequency,
            ratio0 * concert_pitch0,
        )
        self.assertAlmostEqual(
            music_parameters.JustIntonationPitch(ratio1, concert_pitch1).frequency,
            ratio1 * concert_pitch1,
        )
        self.assertAlmostEqual(
            music_parameters.JustIntonationPitch(ratio2, concert_pitch2).frequency,
            ratio2 * concert_pitch2,
        )

    def test_property_ratio(self):
        ratio0 = fractions.Fraction(3, 2)
        ratio1 = fractions.Fraction(25, 1)
        ratio2 = fractions.Fraction(11, 9)
        self.assertEqual(
            music_parameters.JustIntonationPitch(ratio0).ratio,
            ratio0,
        )
        self.assertEqual(
            music_parameters.JustIntonationPitch(ratio1).ratio,
            ratio1,
        )
        self.assertEqual(
            music_parameters.JustIntonationPitch(ratio2).ratio,
            ratio2,
        )

    def test_property_closest_pythagorean_pitch(self):
        self.assertEqual(
            music_parameters.JustIntonationPitch("5/4").closest_pythagorean_interval,
            music_parameters.JustIntonationPitch("81/64"),
        )
        self.assertEqual(
            music_parameters.JustIntonationPitch("11/8").closest_pythagorean_interval,
            music_parameters.JustIntonationPitch("4/3"),
        )
        self.assertEqual(
            music_parameters.JustIntonationPitch("8/7").closest_pythagorean_interval,
            music_parameters.JustIntonationPitch("9/8"),
        )

    def test_property_cent_deviation_from_closest_western_pitch_class(self):
        self.assertEqual(
            round(
                music_parameters.JustIntonationPitch(
                    "5/4"
                ).cent_deviation_from_closest_western_pitch_class
            ),
            -14,
        )
        self.assertEqual(
            round(
                music_parameters.JustIntonationPitch(
                    "5/3"
                ).cent_deviation_from_closest_western_pitch_class
            ),
            -16,
        )
        self.assertEqual(
            round(
                music_parameters.JustIntonationPitch(
                    "9/8"
                ).cent_deviation_from_closest_western_pitch_class
            ),
            4,
        )
        self.assertEqual(
            round(
                music_parameters.JustIntonationPitch(
                    "11/8"
                ).cent_deviation_from_closest_western_pitch_class
            ),
            51,
        )

    def test_count_accidentals(self):
        self.assertEqual(
            music_parameters.JustIntonationPitch._count_accidentals("f"), -1
        )
        self.assertEqual(
            music_parameters.JustIntonationPitch._count_accidentals("s"), 1
        )
        self.assertEqual(
            music_parameters.JustIntonationPitch._count_accidentals("sss"), 3
        )
        self.assertEqual(music_parameters.JustIntonationPitch._count_accidentals(""), 0)
        self.assertEqual(
            music_parameters.JustIntonationPitch._count_accidentals("ssf"), 1
        )

    def test_get_accidentals(self):
        self.assertEqual(music_parameters.JustIntonationPitch._get_accidentals(2), "ss")
        self.assertEqual(
            music_parameters.JustIntonationPitch._get_accidentals(-2), "ff"
        )
        self.assertEqual(music_parameters.JustIntonationPitch._get_accidentals(0), "")
        self.assertEqual(music_parameters.JustIntonationPitch._get_accidentals(-1), "f")

    def test_conversion_to_float(self):
        ratio0 = fractions.Fraction(3, 2)
        ratio1 = fractions.Fraction(25, 1)
        ratio2 = fractions.Fraction(11, 9)
        self.assertEqual(
            float(music_parameters.JustIntonationPitch(ratio0)),
            float(ratio0),
        )
        self.assertEqual(
            float(music_parameters.JustIntonationPitch(ratio1)),
            float(ratio1),
        )
        self.assertEqual(
            float(music_parameters.JustIntonationPitch(ratio2)),
            float(ratio2),
        )

    def test_octave(self):
        jip0 = music_parameters.JustIntonationPitch("3/1")
        jip1 = music_parameters.JustIntonationPitch("1/1")
        jip2 = music_parameters.JustIntonationPitch("5/8")
        jip3 = music_parameters.JustIntonationPitch("5/16")
        jip4 = music_parameters.JustIntonationPitch("15/8")
        jip5 = music_parameters.JustIntonationPitch("2/1")
        jip6 = music_parameters.JustIntonationPitch("1/2")
        self.assertEqual(jip0.octave, 1)
        self.assertEqual(jip1.octave, 0)
        self.assertEqual(jip2.octave, -1)
        self.assertEqual(jip3.octave, -2)
        self.assertEqual(jip4.octave, 0)
        self.assertEqual(jip5.octave, 1)
        self.assertEqual(jip6.octave, -1)

    def test_harmonic(self):
        jip0 = music_parameters.JustIntonationPitch([-1, 1])
        jip1 = music_parameters.JustIntonationPitch([-2, 0, 1])
        jip2 = music_parameters.JustIntonationPitch([0, 0, 0, -1, 1])
        jip3 = music_parameters.JustIntonationPitch([2, -1])
        jip4 = music_parameters.JustIntonationPitch([4, 0, 0, -1])
        jip5 = music_parameters.JustIntonationPitch([])
        self.assertEqual(jip0.harmonic, 3)
        self.assertEqual(jip1.harmonic, 5)
        self.assertEqual(jip2.harmonic, 0)
        self.assertEqual(jip3.harmonic, -3)
        self.assertEqual(jip4.harmonic, -7)
        self.assertEqual(jip5.harmonic, 1)

    def test_tonality(self):
        jip0 = music_parameters.JustIntonationPitch([0, 1])
        jip1 = music_parameters.JustIntonationPitch([0, -1])
        jip2 = music_parameters.JustIntonationPitch([0, 1, -1])
        jip3 = music_parameters.JustIntonationPitch([0, -2, 0, 0, 1])
        jip4 = music_parameters.JustIntonationPitch([0, 0])
        self.assertEqual(jip0.tonality, True)
        self.assertEqual(jip1.tonality, False)
        self.assertEqual(jip2.tonality, False)
        self.assertEqual(jip3.tonality, True)
        self.assertEqual(jip4.tonality, True)

    def test_indigestibility(self):
        self.assertEqual(music_parameters.JustIntonationPitch._indigestibility(1), 0)
        self.assertEqual(music_parameters.JustIntonationPitch._indigestibility(2), 1)
        self.assertEqual(music_parameters.JustIntonationPitch._indigestibility(4), 2)
        self.assertEqual(music_parameters.JustIntonationPitch._indigestibility(5), 6.4)
        self.assertEqual(
            music_parameters.JustIntonationPitch._indigestibility(6), 3.6666666666666665
        )
        self.assertEqual(music_parameters.JustIntonationPitch._indigestibility(8), 3)

    def test_harmonicity_barlow(self):
        jip0 = music_parameters.JustIntonationPitch(
            (
                -1,
                1,
            )
        )
        jip1 = music_parameters.JustIntonationPitch([])
        jip2 = music_parameters.JustIntonationPitch((-2, 0, 1))
        jip3 = music_parameters.JustIntonationPitch((3, 0, -1))
        self.assertEqual(jip0.harmonicity_barlow, 0.27272727272727276)
        self.assertEqual(jip1.harmonicity_barlow, float("inf"))
        self.assertEqual(jip2.harmonicity_barlow, 0.11904761904761904)
        self.assertEqual(jip3.harmonicity_barlow, -0.10638297872340426)

    def test_harmonicity_euler(self):
        jip0 = music_parameters.JustIntonationPitch(
            (
                -1,
                1,
            )
        )
        jip1 = music_parameters.JustIntonationPitch([])
        jip2 = music_parameters.JustIntonationPitch((-2, 0, 1))
        jip3 = music_parameters.JustIntonationPitch((3, 0, -1))
        self.assertEqual(jip0.harmonicity_euler, 4)
        self.assertEqual(jip1.harmonicity_euler, 1)
        self.assertEqual(jip2.harmonicity_euler, 7)
        self.assertEqual(jip3.harmonicity_euler, 8)

    def test_harmonicity_tenney(self):
        jip0 = music_parameters.JustIntonationPitch(
            (
                -1,
                1,
            )
        )
        jip1 = music_parameters.JustIntonationPitch([])
        jip2 = music_parameters.JustIntonationPitch((-2, 0, 1))
        jip3 = music_parameters.JustIntonationPitch((3, 0, -1))
        self.assertEqual(jip0.harmonicity_tenney, 2.584962500721156)
        self.assertEqual(jip1.harmonicity_tenney, 0)
        self.assertEqual(jip2.harmonicity_tenney, 4.321928094887363)
        self.assertEqual(jip3.harmonicity_tenney, 5.321928094887363)

    def test_harmonicity_vogel(self):
        jip0 = music_parameters.JustIntonationPitch(
            (
                -1,
                1,
            )
        )
        jip1 = music_parameters.JustIntonationPitch([])
        jip2 = music_parameters.JustIntonationPitch((-2, 0, 1))
        jip3 = music_parameters.JustIntonationPitch((3, 0, -1))
        self.assertEqual(jip0.harmonicity_vogel, 4)
        self.assertEqual(jip1.harmonicity_vogel, 1)
        self.assertEqual(jip2.harmonicity_vogel, 7)
        self.assertEqual(jip3.harmonicity_vogel, 8)

    def test_harmonicity_wilson(self):
        jip0 = music_parameters.JustIntonationPitch(
            (
                -1,
                1,
            )
        )
        jip1 = music_parameters.JustIntonationPitch([])
        jip2 = music_parameters.JustIntonationPitch((-2, 0, 1))
        jip3 = music_parameters.JustIntonationPitch((3, 0, -1))
        self.assertEqual(jip0.harmonicity_wilson, 3)
        self.assertEqual(jip1.harmonicity_wilson, 1)
        self.assertEqual(jip2.harmonicity_wilson, 5)
        self.assertEqual(jip3.harmonicity_wilson, 5)

    def test_operator_overload_add(self):
        jip0 = music_parameters.JustIntonationPitch("3/2")
        jip1 = music_parameters.JustIntonationPitch("5/4")
        jip2 = music_parameters.JustIntonationPitch("3/1")
        jip0plus1 = music_parameters.JustIntonationPitch("15/8")
        jip0plus2 = music_parameters.JustIntonationPitch("9/2")
        jip1plus2 = music_parameters.JustIntonationPitch("15/4")
        self.assertEqual(jip0 + jip1, jip0plus1)
        self.assertEqual(jip0 + jip2, jip0plus2)
        self.assertEqual(jip1 + jip2, jip1plus2)

    def test_operator_overload_sub(self):
        jip0 = music_parameters.JustIntonationPitch("3/2")
        jip1 = music_parameters.JustIntonationPitch("5/4")
        jip2 = music_parameters.JustIntonationPitch("3/1")
        jip0minus1 = music_parameters.JustIntonationPitch("6/5")
        jip0minus2 = music_parameters.JustIntonationPitch("1/2")
        jip1minus2 = music_parameters.JustIntonationPitch("5/12")
        self.assertEqual(jip0 - jip1, jip0minus1)
        self.assertEqual(jip0 - jip2, jip0minus2)
        self.assertEqual(jip1 - jip2, jip1minus2)

    def test_operator_overload_abs(self):
        jip0 = music_parameters.JustIntonationPitch("1/3")
        jip0_abs = music_parameters.JustIntonationPitch("3/1")
        jip1 = music_parameters.JustIntonationPitch("5/7")
        jip1_abs = music_parameters.JustIntonationPitch("7/5")
        self.assertEqual(abs(jip0), jip0_abs)
        self.assertEqual(abs(jip1), jip1_abs)

    def test_add(self):
        jip0 = music_parameters.JustIntonationPitch("3/2")
        jip1 = music_parameters.JustIntonationPitch("5/4")
        jip2 = music_parameters.JustIntonationPitch("3/1")
        jip0.add(jip1)
        jip1.add(jip2)
        jip0plus1 = music_parameters.JustIntonationPitch("15/8")
        jip1plus2 = music_parameters.JustIntonationPitch("15/4")
        self.assertEqual(jip0, jip0plus1)
        self.assertEqual(jip1, jip1plus2)

    def test_subtract(self):
        jip0 = music_parameters.JustIntonationPitch("3/2")
        jip1 = music_parameters.JustIntonationPitch("5/4")
        jip2 = music_parameters.JustIntonationPitch("3/1")
        jip0.subtract(jip1)
        jip1.subtract(jip2)
        jip0minus1 = music_parameters.JustIntonationPitch("6/5")
        jip1minus2 = music_parameters.JustIntonationPitch("5/12")
        self.assertEqual(jip0, jip0minus1)
        self.assertEqual(jip1, jip1minus2)

    def test_inverse(self):
        jip0 = music_parameters.JustIntonationPitch("3/2")
        jip0inverse = music_parameters.JustIntonationPitch("2/3")
        jip1 = music_parameters.JustIntonationPitch("7/1")
        jip1inverse = music_parameters.JustIntonationPitch("1/7")
        jip2 = music_parameters.JustIntonationPitch("9/11")
        jip2inverse = music_parameters.JustIntonationPitch("11/9")

        jip0.inverse()
        jip1.inverse()

        self.assertEqual(jip0, jip0inverse)
        self.assertEqual(jip1, jip1inverse)
        self.assertEqual(jip2.inverse(mutate=False), jip2inverse)

    def test_normalize(self):
        jip0 = music_parameters.JustIntonationPitch("3/1")
        jip0normalized = music_parameters.JustIntonationPitch("3/2")
        jip1 = music_parameters.JustIntonationPitch("5/6")
        jip1normalized = music_parameters.JustIntonationPitch("5/3")
        jip2 = music_parameters.JustIntonationPitch("27/7")
        jip2normalized = music_parameters.JustIntonationPitch("27/14")

        jip0.normalize()
        jip1.normalize()

        self.assertEqual(jip0, jip0normalized)
        self.assertEqual(jip1, jip1normalized)
        self.assertEqual(jip2.normalize(mutate=False), jip2normalized)

    def test_register(self):
        jip0 = music_parameters.JustIntonationPitch("3/1")
        jip0registered = music_parameters.JustIntonationPitch("3/2")
        jip1 = music_parameters.JustIntonationPitch("5/3")
        jip1registered = music_parameters.JustIntonationPitch("5/12")
        jip2 = music_parameters.JustIntonationPitch("1/1")
        jip2registered = music_parameters.JustIntonationPitch("4/1")

        jip0.register(0)
        jip1.register(-2)

        self.assertEqual(jip0, jip0registered)
        self.assertEqual(jip1, jip1registered)
        self.assertEqual(jip2.register(2, mutate=False), jip2registered)

    def test_move_to_closest_register(self):
        jip0 = music_parameters.JustIntonationPitch("3/1")
        jip0_reference = music_parameters.JustIntonationPitch("5/4")
        jip0_closest = music_parameters.JustIntonationPitch("3/2")

        jip1 = music_parameters.JustIntonationPitch("7/1")
        jip1_reference = music_parameters.JustIntonationPitch("1/1")
        jip1_closest = music_parameters.JustIntonationPitch("7/8")

        jip2 = music_parameters.JustIntonationPitch("1/1")
        jip2_reference = music_parameters.JustIntonationPitch("7/4")
        jip2_closest = music_parameters.JustIntonationPitch("2/1")

        jip2.move_to_closest_register(jip2_reference)

        self.assertEqual(
            jip0.move_to_closest_register(jip0_reference, mutate=False), jip0_closest
        )
        self.assertEqual(
            jip1.move_to_closest_register(jip1_reference, mutate=False), jip1_closest
        )
        self.assertEqual(jip2, jip2_closest)

    def test_get_closest_pythagorean_pitch_name(self):
        self.assertEqual(
            music_parameters.JustIntonationPitch(
                "7/4"
            ).get_closest_pythagorean_pitch_name("c"),
            "bf",
        )
        self.assertEqual(
            music_parameters.JustIntonationPitch(
                "5/4"
            ).get_closest_pythagorean_pitch_name("c"),
            "e",
        )
        self.assertEqual(
            music_parameters.JustIntonationPitch(
                "5/4"
            ).get_closest_pythagorean_pitch_name("a"),
            "cs",
        )
        self.assertEqual(
            music_parameters.JustIntonationPitch(
                "4/5"
            ).get_closest_pythagorean_pitch_name("c"),
            "af",
        )
        self.assertEqual(
            music_parameters.JustIntonationPitch(
                "1/5"
            ).get_closest_pythagorean_pitch_name("c"),
            "af",
        )
        self.assertEqual(
            music_parameters.JustIntonationPitch(
                "128/25"
            ).get_closest_pythagorean_pitch_name("c"),
            "ff",
        )
        self.assertEqual(
            music_parameters.JustIntonationPitch(
                "11/8"
            ).get_closest_pythagorean_pitch_name("e"),
            "a",
        )

    def test_intersection(self):
        p0 = music_parameters.JustIntonationPitch("5/3")
        p0.intersection(music_parameters.JustIntonationPitch("7/6"))
        self.assertEqual(p0, music_parameters.JustIntonationPitch("1/3"))

        p1 = music_parameters.JustIntonationPitch("27/1")
        p1.intersection(music_parameters.JustIntonationPitch("9/1"))
        self.assertEqual(p1, music_parameters.JustIntonationPitch("9/1"))

        p2 = music_parameters.JustIntonationPitch("11/15")
        p2.intersection(music_parameters.JustIntonationPitch("11/5"))
        self.assertEqual(p2, music_parameters.JustIntonationPitch("11/5"))

        p3 = music_parameters.JustIntonationPitch("15/8")
        p3.intersection(music_parameters.JustIntonationPitch("21/16"))
        self.assertEqual(p3, music_parameters.JustIntonationPitch("3/8"))

    def test_intersection_strict(self):
        p0 = music_parameters.JustIntonationPitch("5/3")
        p0.intersection(music_parameters.JustIntonationPitch("7/6"), strict=True)
        self.assertEqual(p0, music_parameters.JustIntonationPitch("1/3"))

        p1 = music_parameters.JustIntonationPitch("27/1")
        p1.intersection(music_parameters.JustIntonationPitch("9/1"), strict=True)
        self.assertEqual(p1, music_parameters.JustIntonationPitch("1/1"))

    def test_equal(self):
        for pitch, any_object, expected_value in (
            (
                music_parameters.JustIntonationPitch("3/2"),
                music_parameters.JustIntonationPitch("3/2"),
                True,
            ),
            (
                music_parameters.JustIntonationPitch("3/2"),
                music_parameters.JustIntonationPitch("3/1"),
                False,
            ),
            (
                music_parameters.JustIntonationPitch("1/1"),
                music_parameters.WesternPitch("a", 4),
                True,
            ),
            (
                music_parameters.JustIntonationPitch("7/4"),
                fractions.Fraction(7, 4),
                False,
            ),
        ):
            self.assertEqual(pitch == any_object, expected_value)


if __name__ == "__main__":
    unittest.main()
