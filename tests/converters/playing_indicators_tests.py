import unittest

try:
    import quicktions as fractions
except ImportError:
    import fractions

from mutwo import core_events
from mutwo import core_parameters
from mutwo import music_converters
from mutwo import music_events


class ArpeggioConverterTest(unittest.TestCase):
    def test_convert(self):
        converter = music_converters.ArpeggioConverter(
            duration_for_each_attack=fractions.Fraction(1, 10)
        )
        note_like = music_events.NoteLike("c g e b", duration=5)
        note_like.playing_indicator_collection.arpeggio.direction = "up"
        arpeggio = core_events.SequentialEvent(
            [
                music_events.NoteLike(pitch, duration)
                for pitch, duration in zip(
                    "c e g b".split(" "),
                    (
                        fractions.Fraction(1, 10),
                        fractions.Fraction(1, 10),
                        fractions.Fraction(1, 10),
                        fractions.Fraction(47, 10),
                    ),
                )
            ]
        )
        for note in arpeggio:
            note.playing_indicator_collection.arpeggio.direction = "up"

        self.assertEqual(converter.convert(note_like), arpeggio)


class PlayingIndicatorsConverterTest(unittest.TestCase):
    def setUp(self):
        self.default_note_like = music_events.NoteLike("c g e b", duration=5)
        self.default_note_like.playing_indicator_collection.arpeggio.direction = "up"
        self.default_note_like_arpeggio_resolution = core_events.SequentialEvent(
            [
                music_events.NoteLike(pitch, duration)
                for pitch, duration in zip(
                    "c e g b".split(" "),
                    (
                        fractions.Fraction(1, 10),
                        fractions.Fraction(1, 10),
                        fractions.Fraction(1, 10),
                        fractions.Fraction(47, 10),
                    ),
                )
            ]
        )
        for note_like in self.default_note_like_arpeggio_resolution:
            note_like.playing_indicator_collection.arpeggio.direction = "up"
        self.default_converter = music_converters.PlayingIndicatorsConverter(
            [
                music_converters.ArpeggioConverter(
                    duration_for_each_attack=core_parameters.DirectDuration(
                        fractions.Fraction(1, 10)
                    )
                )
            ]
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


class OptionalConverterTest(unittest.TestCase):
    def test_convert(self):
        o = music_converters.OptionalConverter
        seq = core_events.SequentialEvent
        duration = 5
        note_like = music_events.NoteLike("c", duration=duration)
        note_like.playing_indicator_collection.optional = True
        self.assertEqual(
            o(likelihood=0).convert(note_like),
            seq([core_events.SimpleEvent(duration=duration)]),
        )
        self.assertEqual(o(likelihood=1).convert(note_like), seq([note_like]))


if __name__ == "__main__":
    unittest.main()
