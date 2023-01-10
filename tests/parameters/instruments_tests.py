import unittest

import ranges

from mutwo import music_parameters


class NaturalHarmonicTest(unittest.TestCase):
    def setUp(self):
        self.string = music_parameters.String(0, music_parameters.WesternPitch("g", 3))
        self.natural_harmonic = music_parameters.NaturalHarmonic(3, self.string)

    def test_interval(self):
        self.assertEqual(
            self.natural_harmonic.interval, music_parameters.JustIntonationPitch("3/1")
        )

    def test_pitch(self):
        self.assertAlmostEqual(
            self.natural_harmonic.pitch.frequency,
            (
                # It's a fifth + two octaves higher,
                music_parameters.WesternPitch("d", 5)
                # but with a just interval and not a tempered one
                # (2 ct difference).
                + music_parameters.DirectPitchInterval(2)
            ).frequency,
            1,
        )

    def test_node_tuple(self):
        self.assertEqual(
            self.natural_harmonic.node_tuple,
            (
                music_parameters.NaturalHarmonic.Node(
                    music_parameters.JustIntonationPitch("3/2"),
                    self.natural_harmonic,
                    self.string,
                ),
                music_parameters.NaturalHarmonic.Node(
                    music_parameters.JustIntonationPitch("3/1"),
                    self.natural_harmonic,
                    self.string,
                ),
            ),
        )


class StringTest(unittest.TestCase):
    def setUp(self):
        self.string = music_parameters.String(0, music_parameters.WesternPitch("g", 3))

    def test_index_to_natural_harmonic(self):
        h, s = music_parameters.NaturalHarmonic, self.string
        for index, h_ok in ((1, h(1, s)), (11, h(11, s)), (421, h(421, s))):
            with self.subTest(index=index):
                self.assertEqual(self.string.index_to_natural_harmonic(index), h_ok)

    def test_natural_harmonic_tuple(self):
        def h(i):
            return music_parameters.NaturalHarmonic(i, self.string)

        self.assertEqual(
            self.string.natural_harmonic_tuple, (h(2), h(3), h(4), h(5), h(6))
        )


class StringInstrumentMixinTest(unittest.TestCase):
    def setUp(self):
        self.string_instrument_mixin = music_parameters.StringInstrumentMixin(
            (
                music_parameters.String(
                    0,
                    music_parameters.WesternPitch("g", 3), max_natural_harmonic_index=3
                ),
            )
        )

    def test_harmonic_pitch_tuple(self):
        self.assertEqual(
            tuple(
                music_parameters.WesternPitch(p.pitch_class_name, p.octave)
                for p in self.string_instrument_mixin.harmonic_pitch_tuple
            ),
            (
                music_parameters.WesternPitch("g", 4),
                music_parameters.WesternPitch("d", 5),
            ),
        )

    def test_pitch_to_natural_harmonic_tuple(self):
        self.assertEqual(
            self.string_instrument_mixin.pitch_to_natural_harmonic_tuple(
                music_parameters.WesternPitch("d", 5)
            ),
            (
                music_parameters.NaturalHarmonic(
                    3, self.string_instrument_mixin.string_tuple[0]
                ),
            ),
        )

    def test_get_harmonic_pitch_variant_tuple(self):
        g = self.string_instrument_mixin.get_harmonic_pitch_variant_tuple
        self.assertEqual(
            g(music_parameters.WesternPitch("d", 2)),
            (music_parameters.WesternPitch("d", 5),),
        )
        self.assertEqual(
            g(
                music_parameters.WesternPitch("d", 2),
                tolerance=music_parameters.DirectPitchInterval(0),
            ),
            tuple([]),
        )


class UnpitchedInstrumentTest(unittest.TestCase):
    def setUp(self):
        self.unpitched_instrument = music_parameters.UnpitchedInstrument("test", "t")

    def test_is_pitched(self):
        self.assertFalse(self.unpitched_instrument.is_pitched)

    def test_name(self):
        self.assertEqual(self.unpitched_instrument.name, "test")

    def test_short_name(self):
        self.assertEqual(self.unpitched_instrument.short_name, "t")


class ContinuousPitchedInstrumentTest(unittest.TestCase):
    def setUp(self):
        self.continuous_pitched_instrument = (
            music_parameters.ContinuousPitchedInstrument(
                music_parameters.OctaveAmbitus(
                    music_parameters.WesternPitch("g", 3),
                    music_parameters.WesternPitch("e", 7),
                ),
                "violin",
                "vl.",
            )
        )

    def test_is_pitched(self):
        self.assertTrue(self.continuous_pitched_instrument.is_pitched)

    def test_contains(self):
        self.assertFalse(
            music_parameters.WesternPitch("c", 8) in self.continuous_pitched_instrument
        )
        self.assertTrue(
            music_parameters.WesternPitch("g", 4) in self.continuous_pitched_instrument
        )

    def test_pitch_ambitus(self):
        self.assertEqual(
            self.continuous_pitched_instrument.pitch_ambitus.minima_pitch,
            music_parameters.WesternPitch("g", 3),
        )
        self.assertEqual(
            self.continuous_pitched_instrument.pitch_ambitus.maxima_pitch,
            music_parameters.WesternPitch("e", 7),
        )

    def test_name(self):
        self.assertEqual(self.continuous_pitched_instrument.name, "violin")

    def test_short_name(self):
        self.assertEqual(self.continuous_pitched_instrument.short_name, "vl.")

    def test_pitch_count_range(self):
        self.assertEqual(
            self.continuous_pitched_instrument.pitch_count_range, ranges.Range(1, 2)
        )


class DiscreetPitchedInstrumentTest(unittest.TestCase):
    def setUp(self):
        self.discreet_pitched_instrument = music_parameters.DiscreetPitchedInstrument(
            (
                music_parameters.JustIntonationPitch("1/1"),
                music_parameters.JustIntonationPitch("9/8"),
                music_parameters.JustIntonationPitch("5/4"),
                music_parameters.JustIntonationPitch("3/2"),
                music_parameters.JustIntonationPitch("7/4"),
            ),
            "idiophone",
            "id.",
        )

    def test_pitch_tuple(self):
        self.assertEqual(
            self.discreet_pitched_instrument.pitch_tuple,
            (
                music_parameters.JustIntonationPitch("1/1"),
                music_parameters.JustIntonationPitch("9/8"),
                music_parameters.JustIntonationPitch("5/4"),
                music_parameters.JustIntonationPitch("3/2"),
                music_parameters.JustIntonationPitch("7/4"),
            ),
        )

    def test_pitch_ambitus(self):
        self.assertEqual(
            self.discreet_pitched_instrument.pitch_ambitus.minima_pitch,
            music_parameters.JustIntonationPitch("1/1"),
        )
        self.assertEqual(
            self.discreet_pitched_instrument.pitch_ambitus.maxima_pitch,
            music_parameters.JustIntonationPitch("7/4"),
        )


class OrchestrationTest(unittest.TestCase):
    def setUp(self):
        self.oboe = oboe = music_parameters.Oboe()
        self.clarinet = clarinet = music_parameters.BfClarinet()
        self.orchestration = music_parameters.Orchestration(
            oboe0=oboe, oboe1=oboe, oboe2=oboe, clarinet=clarinet
        )

    def test_fetch_instrument(self):
        self.assertEqual(self.orchestration.oboe0, self.oboe)
        self.assertEqual(self.orchestration.clarinet, self.clarinet)
        self.assertEqual(self.orchestration[-1], self.clarinet)

    def test_get_subset(self):
        subset = self.orchestration.get_subset("oboe0", "clarinet")
        self.assertEqual(len(subset), 2)
        self.assertTrue(hasattr(subset, "oboe0"))
        self.assertTrue(hasattr(subset, "clarinet"))
        self.assertFalse(hasattr(subset, "oboe1"))
        self.assertEqual(subset.oboe0, self.oboe)
        self.assertEqual(subset.clarinet, self.clarinet)
