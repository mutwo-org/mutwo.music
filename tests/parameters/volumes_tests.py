import unittest


from mutwo import music_parameters


class AmplitudeVolumeTest(unittest.TestCase):
    def test_equal(self):
        self.assertEqual(
            music_parameters.AmplitudeVolume(1), music_parameters.AmplitudeVolume(1)
        )
        self.assertEqual(
            music_parameters.AmplitudeVolume(0.3), music_parameters.AmplitudeVolume(0.3)
        )
        self.assertNotEqual(
            music_parameters.AmplitudeVolume(0.5), music_parameters.AmplitudeVolume(0.3)
        )

    def test_comparision(self):
        self.assertLess(
            music_parameters.AmplitudeVolume(0.4), music_parameters.AmplitudeVolume(1)
        )
        self.assertLess(
            music_parameters.AmplitudeVolume(0.1), music_parameters.AmplitudeVolume(0.3)
        )
        self.assertGreater(
            music_parameters.AmplitudeVolume(0.5), music_parameters.AmplitudeVolume(0.3)
        )
        self.assertGreaterEqual(
            music_parameters.AmplitudeVolume(0.3), music_parameters.AmplitudeVolume(0.3)
        )

    def test_midi_velocity(self):
        self.assertEqual(music_parameters.AmplitudeVolume(1).midi_velocity, 127)
        self.assertEqual(music_parameters.AmplitudeVolume(0).midi_velocity, 0)
        self.assertEqual(music_parameters.AmplitudeVolume(0.5).midi_velocity, 107)

    def test_decibel(self):
        self.assertEqual(music_parameters.AmplitudeVolume(1).decibel, 0)
        self.assertEqual(music_parameters.AmplitudeVolume(0).decibel, float("-inf"))
        self.assertAlmostEqual(
            music_parameters.AmplitudeVolume(0.5).decibel, -6, places=1
        )


class DirectVolumeTest(unittest.TestCase):
    def setUp(self):
        self.vol = music_parameters.DirectVolume(-12)

    def test_decibel(self):
        self.assertEqual(self.vol.decibel, -12)

    def test_set_decibel(self):
        self.vol.decibel = -6
        self.assertEqual(self.vol.decibel, -6)

    def test_amplitude(self):
        self.assertEqual(
            self.vol.amplitude,
            music_parameters.abc.Volume.decibel_to_amplitude_ratio(-12),
        )


class FlexVolumeTest(unittest.TestCase):
    def setUp(self):
        self.v = music_parameters.FlexVolume([[0, "mf"], [1, "fff"]])

    def test_decibel(self):
        self.assertEqual(self.v.decibel, self.v[0].volume.decibel)


class WesternVolumeTest(unittest.TestCase):
    def setUp(self):
        self.vol = music_parameters.WesternVolume("p")

    def test_name(self):
        self.assertEqual(self.vol.name, "p")

    def test_set_name(self):
        self.vol.name = "ff"
        self.assertEqual(self.vol.name, "ff")


if __name__ == "__main__":
    unittest.main()
