from __future__ import annotations

import unittest

try:
    import quicktions as fractions  # type: ignore
except ImportError:
    import fractions  # type: ignore

from mutwo import music_parameters


class PitchTest(unittest.TestCase):
    class GenericPitch(music_parameters.abc.Pitch):
        """Pitch only for UnitTest with minimal functionality"""

        def __init__(self, frequency: float, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self._frequency = frequency

        @property
        def frequency(self) -> float:
            return self._frequency

        def add(self, pitch_interval: music_parameters.PitchInterval) -> GenericPitch:
            self._frequency = (
                self.cents_to_ratio(pitch_interval.interval) * self.frequency
            )
            return self

        def subtract(
            self, pitch_interval: music_parameters.PitchInterval
        ) -> GenericPitch:
            self._frequency = self.frequency / self.cents_to_ratio(
                pitch_interval.interval
            )
            return self

    def test_abstract_error(self):
        self.assertRaises(TypeError, music_parameters.abc.Pitch)

    def test_hertz_to_cents(self):
        self.assertEqual(1200, music_parameters.abc.Pitch.hertz_to_cents(440, 880))
        self.assertEqual(-1200, music_parameters.abc.Pitch.hertz_to_cents(880, 440))
        self.assertEqual(0, music_parameters.abc.Pitch.hertz_to_cents(10, 10))
        self.assertEqual(
            702, round(music_parameters.abc.Pitch.hertz_to_cents(440, 440 * 3 / 2))
        )

    def test_ratio_to_cents(self):
        self.assertEqual(
            1200, music_parameters.abc.Pitch.ratio_to_cents(fractions.Fraction(2, 1))
        )
        self.assertEqual(
            -1200, music_parameters.abc.Pitch.ratio_to_cents(fractions.Fraction(1, 2))
        )
        self.assertEqual(
            0, music_parameters.abc.Pitch.ratio_to_cents(fractions.Fraction(1, 1))
        )
        self.assertEqual(
            702,
            round(music_parameters.abc.Pitch.ratio_to_cents(fractions.Fraction(3, 2))),
        )

    def test_cents_to_ratio(self):
        self.assertEqual(
            fractions.Fraction(2, 1), music_parameters.abc.Pitch.cents_to_ratio(1200)
        )
        self.assertEqual(
            fractions.Fraction(1, 2), music_parameters.abc.Pitch.cents_to_ratio(-1200)
        )
        self.assertEqual(
            fractions.Fraction(1, 1), music_parameters.abc.Pitch.cents_to_ratio(0)
        )

    def test_hertz_to_midi_pitch_number(self):
        self.assertEqual(69, music_parameters.abc.Pitch.hertz_to_midi_pitch_number(440))
        self.assertEqual(
            60, round(music_parameters.abc.Pitch.hertz_to_midi_pitch_number(261))
        )


class VolumeTest(unittest.TestCase):
    def test_decibel_to_amplitude_ratio(self):
        self.assertEqual(
            music_parameters.abc.Volume.decibel_to_amplitude_ratio(0),
            1,
        )
        self.assertEqual(
            round(
                music_parameters.abc.Volume.decibel_to_amplitude_ratio(-6),
                2,
            ),
            0.5,
        )
        self.assertEqual(
            round(
                music_parameters.abc.Volume.decibel_to_amplitude_ratio(-12),
                2,
            ),
            0.25,
        )
        # different reference amplitude
        self.assertEqual(
            music_parameters.abc.Volume.decibel_to_amplitude_ratio(0, 0.5),
            0.5,
        )
        self.assertEqual(
            music_parameters.abc.Volume.decibel_to_amplitude_ratio(0, 2),
            2,
        )

    def test_decibel_to_power_ratio(self):
        self.assertEqual(
            music_parameters.abc.Volume.decibel_to_power_ratio(0),
            1,
        )
        self.assertEqual(
            music_parameters.abc.Volume.decibel_to_power_ratio(-6),
            0.251188643150958,
        )
        self.assertEqual(
            music_parameters.abc.Volume.decibel_to_power_ratio(6),
            3.9810717055349722,
        )

    def test_amplitude_ratio_to_decibel(self):
        self.assertEqual(
            music_parameters.abc.Volume.amplitude_ratio_to_decibel(1),
            0,
        )
        self.assertEqual(
            music_parameters.abc.Volume.amplitude_ratio_to_decibel(
                0.5, reference_amplitude=0.5
            ),
            0,
        )
        self.assertAlmostEqual(
            music_parameters.abc.Volume.amplitude_ratio_to_decibel(0.50118),
            -6,
            places=3,
        )
        self.assertAlmostEqual(
            music_parameters.abc.Volume.amplitude_ratio_to_decibel(0.25),
            -12.041,
            places=3,
        )
        self.assertEqual(
            music_parameters.abc.Volume.amplitude_ratio_to_decibel(0),
            float("-inf"),
        )

    def test_power_ratio_to_decibel(self):
        self.assertEqual(
            music_parameters.abc.Volume.power_ratio_to_decibel(1),
            0,
        )
        self.assertEqual(
            music_parameters.abc.Volume.power_ratio_to_decibel(
                0.5, reference_amplitude=0.5
            ),
            0,
        )
        self.assertAlmostEqual(
            music_parameters.abc.Volume.power_ratio_to_decibel(0.25), -6, places=1
        )
        self.assertAlmostEqual(
            music_parameters.abc.Volume.power_ratio_to_decibel(0.06309), -12, places=3
        )
        self.assertEqual(
            music_parameters.abc.Volume.power_ratio_to_decibel(0),
            float("-inf"),
        )

    def test_amplitude_ratio_to_velocity(self):
        amplitude0 = 1
        amplitude1 = 0
        self.assertEqual(
            music_parameters.abc.Volume.amplitude_ratio_to_midi_velocity(amplitude0),
            127,
        )
        self.assertEqual(
            music_parameters.abc.Volume.amplitude_ratio_to_midi_velocity(amplitude1), 0
        )


class PitchAmbitusTest(unittest.TestCase):
    class GenericPitchAmbitus(music_parameters.abc.PitchAmbitus):
        def pitch_to_period(
            self, _: music_parameters.abc.Pitch
        ) -> music_parameters.abc.PitchInterval:
            return music_parameters.DirectPitchInterval(1200)

    def test_get_pitch_variant_tuple(self):
        pitch_ambitus = self.GenericPitchAmbitus(
            music_parameters.DirectPitch(220),
            music_parameters.DirectPitch(880),
        )
        self.assertEqual(
            pitch_ambitus.get_pitch_variant_tuple(music_parameters.DirectPitch(220)),
            (
                music_parameters.DirectPitch(220),
                music_parameters.DirectPitch(440),
                music_parameters.DirectPitch(880),
            ),
        )

    def test_filter_pitch_sequence(self):
        ambitus = music_parameters.OctaveAmbitus(
            music_parameters.JustIntonationPitch("1/2"),
            music_parameters.JustIntonationPitch("2/1"),
        )
        self.assertEqual(
            ambitus.filter_pitch_sequence(
                [
                    music_parameters.JustIntonationPitch("3/8"),
                    music_parameters.JustIntonationPitch("3/4"),
                    music_parameters.JustIntonationPitch("3/2"),
                    music_parameters.JustIntonationPitch("3/1"),
                ]
            ),
            (
                music_parameters.JustIntonationPitch("3/4"),
                music_parameters.JustIntonationPitch("3/2"),
            ),
        )

    def test_contains(self):
        ambitus = music_parameters.OctaveAmbitus(
            music_parameters.JustIntonationPitch("1/2"),
            music_parameters.JustIntonationPitch("2/1"),
        )
        self.assertTrue(music_parameters.JustIntonationPitch("3/2") in ambitus)
        self.assertFalse(music_parameters.JustIntonationPitch("3/1") in ambitus)


if __name__ == "__main__":
    unittest.main()
