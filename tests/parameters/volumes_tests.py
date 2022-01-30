import unittest


from mutwo import music_parameters


class DirectVolumeTest(unittest.TestCase):
    def test_equal(self):
        self.assertEqual(
            music_parameters.DirectVolume(1), music_parameters.DirectVolume(1)
        )
        self.assertEqual(
            music_parameters.DirectVolume(0.3), music_parameters.DirectVolume(0.3)
        )
        self.assertNotEqual(
            music_parameters.DirectVolume(0.5), music_parameters.DirectVolume(0.3)
        )

    def test_comparision(self):
        self.assertLess(
            music_parameters.DirectVolume(0.4), music_parameters.DirectVolume(1)
        )
        self.assertLess(
            music_parameters.DirectVolume(0.1), music_parameters.DirectVolume(0.3)
        )
        self.assertGreater(
            music_parameters.DirectVolume(0.5), music_parameters.DirectVolume(0.3)
        )
        self.assertGreaterEqual(
            music_parameters.DirectVolume(0.3), music_parameters.DirectVolume(0.3)
        )

    def test_midi_velocity(self):
        self.assertEqual(music_parameters.DirectVolume(1).midi_velocity, 127)
        self.assertEqual(music_parameters.DirectVolume(0).midi_velocity, 0)
        self.assertEqual(music_parameters.DirectVolume(0.5).midi_velocity, 107)

    def test_decibel(self):
        self.assertEqual(music_parameters.DirectVolume(1).decibel, 0)
        self.assertEqual(music_parameters.DirectVolume(0).decibel, float("-inf"))
        self.assertAlmostEqual(music_parameters.DirectVolume(0.5).decibel, -6, places=1)


if __name__ == "__main__":
    unittest.main()
