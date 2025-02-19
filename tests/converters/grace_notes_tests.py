import unittest

from mutwo import core_events
from mutwo import music_converters
from mutwo import music_events


class GraceNotesConverterTest(unittest.TestCase):
    def setUp(self):
        self.grace_notes_converter = music_converters.GraceNotesConverter()

    def test_convert_note_like(self):
        note_like = music_events.NoteLike(
            duration=1,
            grace_note_consecution=core_events.Consecution(
                [
                    music_events.NoteLike(duration=0.5),
                    music_events.NoteLike(duration=1),
                ]
            ),
        )
        converted_note_like = self.grace_notes_converter.convert(note_like)

        self.assertEqual(note_like.duration, converted_note_like.duration)
        self.assertEqual(
            len(converted_note_like), 1 + len(note_like.grace_note_consecution)
        )
        self.assertTrue(isinstance(converted_note_like, core_events.Consecution))
        self.assertAlmostEqual(
            converted_note_like[0].duration / converted_note_like[1].duration,
            note_like.grace_note_consecution[0].duration
            / note_like.grace_note_consecution[1].duration,
        )

    def test_convert_consecution(self):
        cns = core_events.Consecution(
            [
                music_events.NoteLike("a"),
                music_events.NoteLike(
                    "e",
                    after_grace_note_consecution=core_events.Consecution(
                        [music_events.NoteLike("f")]
                    ),
                ),
            ]
        )
        converted_cns = self.grace_notes_converter.convert(cns)
        self.assertEqual(cns.duration, converted_cns.duration)
        self.assertEqual(
            len(converted_cns), 3  # two main events + one after grace note
        )


if __name__ == "__main__":
    unittest.main()
