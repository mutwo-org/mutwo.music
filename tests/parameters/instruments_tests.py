import unittest

import ranges

from mutwo import music_parameters


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
        self.orchestration = music_parameters.Orchestration(
            oboe0=music_parameters.constants.OBOE,
            oboe1=music_parameters.constants.OBOE,
            oboe2=music_parameters.constants.OBOE,
            clarinet=music_parameters.constants.BF_CLARINET,
        )

    def test_fetch_instrument(self):
        self.assertEqual(self.orchestration.oboe0, music_parameters.constants.OBOE)
        self.assertEqual(
            self.orchestration.clarinet, music_parameters.constants.BF_CLARINET
        )
        self.assertEqual(self.orchestration[-1], music_parameters.constants.BF_CLARINET)

    def test_get_subset(self):
        subset = self.orchestration.get_subset("oboe0", "clarinet")
        self.assertEqual(len(subset), 2)
        self.assertTrue(hasattr(subset, "oboe0"))
        self.assertTrue(hasattr(subset, "clarinet"))
        self.assertFalse(hasattr(subset, "oboe1"))
        self.assertEqual(subset.oboe0, music_parameters.constants.OBOE)
        self.assertEqual(subset.clarinet, music_parameters.constants.BF_CLARINET)
