import unittest

from mutwo import core_events
from mutwo import music_converters
from mutwo import music_events


class ArpeggioConverterTest(unittest.TestCase):
    def test_convert(self):
        converter = music_converters.ArpeggioConverter(duration_for_each_attack=0.1)
        note_like = music_events.NoteLike("c g e b", duration=5)
        note_like.playing_indicator_collection.arpeggio.direction = "up"
        arpeggio = core_events.SequentialEvent(
            [
                music_events.NoteLike(pitch, duration)
                for pitch, duration in zip("c e g b".split(" "), (0.1, 0.1, 0.1, 4.7))
            ]
        )
        for note in arpeggio:
            note.playing_indicator_collection.arpeggio.direction = "up"

        self.assertEqual(converter.convert(note_like), arpeggio)


class PlayingIndicatorsConverterTest(unittest.TestCase):
    def setUp(cls):
        cls.default_note_like = music_events.NoteLike("c g e b", duration=5)
        cls.default_note_like.playing_indicator_collection.arpeggio.direction = "up"
        cls.default_note_like_arpeggio_resolution = core_events.SequentialEvent(
            [
                music_events.NoteLike(pitch, duration)
                for pitch, duration in zip("c e g b".split(" "), (0.1, 0.1, 0.1, 4.7))
            ]
        )
        for note_like in cls.default_note_like_arpeggio_resolution:
            note_like.playing_indicator_collection.arpeggio.direction = "up"
        cls.default_converter = music_converters.PlayingIndicatorsConverter(
            [music_converters.ArpeggioConverter(duration_for_each_attack=0.1)]
        )

    def test_convert_note_like(self):
        self.assertEqual(
            self.default_converter.convert(self.default_note_like),
            self.default_note_like_arpeggio_resolution,
        )

    def test_convert_sequential_event(self):
        self.assertEqual(
            self.default_converter.convert(
                core_events.SequentialEvent([self.default_note_like])
            ),
            core_events.SequentialEvent([self.default_note_like_arpeggio_resolution]),
        )

    def test_convert_simultaneous_event(self):
        self.assertEqual(
            self.default_converter.convert(
                core_events.SimultaneousEvent([self.default_note_like])
            ),
            core_events.SimultaneousEvent([self.default_note_like_arpeggio_resolution]),
        )


if __name__ == "__main__":
    unittest.main()
