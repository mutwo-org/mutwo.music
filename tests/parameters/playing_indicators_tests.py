import dataclasses
import unittest

from mutwo import music_parameters


class PlayingIndicatorCollectionTest(unittest.TestCase):
    def setUp(self):
        self.playing_indicator_collection = (
            music_parameters.PlayingIndicatorCollection()
        )

    def test_syntactic_sugar_setter(self):
        # Normal setting of explicit playing indicators
        self.playing_indicator_collection.tie.is_active = False
        self.assertEqual(self.playing_indicator_collection.tie.is_active, False)

        # Syntactic sugar for setting explicit playing indicators
        self.playing_indicator_collection.tie = True
        self.assertEqual(self.playing_indicator_collection.tie.is_active, True)

        self.playing_indicator_collection.tie.is_active = False
