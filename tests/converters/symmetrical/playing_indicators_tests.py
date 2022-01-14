import unittest

from mutwo.core.events import basic

from mutwo.ext.converters import symmetrical
from mutwo.ext.events import music


class ArpeggioConverterTest(unittest.TestCase):
    def test_convert(self):
        converter = symmetrical.playing_indicators.ArpeggioConverter(
            duration_for_each_attack=0.1
        )
        note_like = music.NoteLike("c g e b", duration=5)
        note_like.playing_indicator_collection.arpeggio.direction = "up"
        arpeggio = basic.SequentialEvent(
            [
                music.NoteLike(pitch, duration)
                for pitch, duration in zip("c e g b".split(" "), (0.1, 0.1, 0.1, 4.7))
            ]
        )
        for note in arpeggio:
            note.playing_indicator_collection.arpeggio.direction = "up"

        self.assertEqual(converter.convert(note_like), arpeggio)


class PlayingIndicatorsConverterTest(unittest.TestCase):
    def setUp(cls):
        cls.default_note_like = music.NoteLike("c g e b", duration=5)
        cls.default_note_like.playing_indicator_collection.arpeggio.direction = "up"
        cls.default_note_like_arpeggio_resolution = basic.SequentialEvent(
            [
                music.NoteLike(pitch, duration)
                for pitch, duration in zip("c e g b".split(" "), (0.1, 0.1, 0.1, 4.7))
            ]
        )
        for note_like in cls.default_note_like_arpeggio_resolution:
            note_like.playing_indicator_collection.arpeggio.direction = "up"
        cls.default_converter = (
            symmetrical.playing_indicators.PlayingIndicatorsConverter(
                [
                    symmetrical.playing_indicators.ArpeggioConverter(
                        duration_for_each_attack=0.1
                    )
                ]
            )
        )

    def test_convert_note_like(self):
        self.assertEqual(
            self.default_converter.convert(self.default_note_like),
            self.default_note_like_arpeggio_resolution,
        )

    def test_convert_sequential_event(self):
        self.assertEqual(
            self.default_converter.convert(
                basic.SequentialEvent([self.default_note_like])
            ),
            basic.SequentialEvent([self.default_note_like_arpeggio_resolution]),
        )

    def test_convert_simultaneous_event(self):
        self.assertEqual(
            self.default_converter.convert(
                basic.SimultaneousEvent([self.default_note_like])
            ),
            basic.SimultaneousEvent([self.default_note_like_arpeggio_resolution]),
        )


if __name__ == "__main__":
    unittest.main()
