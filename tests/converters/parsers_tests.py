import unittest

from mutwo import core_events
from mutwo import music_converters
from mutwo import music_events
from mutwo import music_parameters


class SimpleEventToPitchListTest(unittest.TestCase):
    def setUp(cls):
        cls.converter = music_converters.SimpleEventToPitchList()

    def test_convert_with_attribute(self):
        self.assertEqual(
            self.converter(music_events.NoteLike("1/1 3/2")),
            [
                music_parameters.JustIntonationPitch("1/1"),
                music_parameters.JustIntonationPitch("3/2"),
            ],
        )

    def test_convert_without_attribute(self):
        self.assertEqual(self.converter(core_events.SimpleEvent(10)), [])


class SimpleEventToVolumeTest(unittest.TestCase):
    def setUp(cls):
        cls.converter = music_converters.SimpleEventToVolume()

    def test_convert_with_attribute(self):
        self.assertEqual(
            self.converter(music_events.NoteLike(volume="fff")),
            music_parameters.WesternVolume("fff"),
        )

    def test_convert_without_attribute(self):
        self.assertEqual(
            self.converter(core_events.SimpleEvent(10)),
            music_parameters.DirectVolume(0),
        )


class SimpleEventToPlayingIndicatorCollectionTest(unittest.TestCase):
    def setUp(cls):
        cls.converter = music_converters.SimpleEventToPlayingIndicatorCollection()

    def test_convert_with_attribute(self):
        self.assertEqual(
            self.converter(music_events.NoteLike()),
            music_events.configurations.DEFAULT_PLAYING_INDICATORS_COLLECTION_CLASS(),
        )

    def test_convert_without_attribute(self):
        self.assertEqual(
            self.converter(core_events.SimpleEvent(10)),
            music_events.configurations.DEFAULT_PLAYING_INDICATORS_COLLECTION_CLASS(),
        )


class SimpleEventToNotationIndicatorCollectionTest(unittest.TestCase):
    def setUp(cls):
        cls.converter = music_converters.SimpleEventToNotationIndicatorCollection()

    def test_convert_with_attribute(self):
        self.assertEqual(
            self.converter(music_events.NoteLike()),
            music_events.configurations.DEFAULT_NOTATION_INDICATORS_COLLECTION_CLASS(),
        )

    def test_convert_without_attribute(self):
        self.assertEqual(
            self.converter(core_events.SimpleEvent(10)),
            music_events.configurations.DEFAULT_NOTATION_INDICATORS_COLLECTION_CLASS(),
        )

    def test_convert_with_default_value_change(self):
        """Ensure changing the default value affects the converter"""

        default_notation_indicators_collection_class = (
            music_events.configurations.DEFAULT_NOTATION_INDICATORS_COLLECTION_CLASS
        )
        music_events.configurations.DEFAULT_NOTATION_INDICATORS_COLLECTION_CLASS = (
            lambda: "TEST"
        )
        self.assertEqual(self.converter(core_events.SimpleEvent(10)), "TEST")
        # Cleanup
        music_events.configurations.DEFAULT_NOTATION_INDICATORS_COLLECTION_CLASS = (
            default_notation_indicators_collection_class
        )


class SimpleEventToGraceOrAfterGraceNoteSequentialEventTestMixin(object):
    def test_convert_without_attribute(self):
        self.assertEqual(
            self.converter(core_events.SimpleEvent(10)),
            core_events.SequentialEvent([]),
        )


class SimpleEventToGraceNoteSequentialEventTest(
    unittest.TestCase, SimpleEventToGraceOrAfterGraceNoteSequentialEventTestMixin
):
    def setUp(cls):
        cls.converter = music_converters.SimpleEventToGraceNoteSequentialEvent()

    def test_convert_with_attribute(self):
        grace_note_sequential_event = core_events.SequentialEvent(
            [music_events.NoteLike("c")]
        )
        self.assertEqual(
            self.converter(
                music_events.NoteLike(
                    grace_note_sequential_event=grace_note_sequential_event
                )
            ),
            grace_note_sequential_event,
        )

    def test_convert_without_attribute(self):
        self.assertEqual(
            self.converter(core_events.SimpleEvent(10)),
            core_events.SequentialEvent([]),
        )


class SimpleEventToAfterGraceNoteSequentialEventTest(
    unittest.TestCase, SimpleEventToGraceOrAfterGraceNoteSequentialEventTestMixin
):
    def setUp(cls):
        cls.converter = music_converters.SimpleEventToAfterGraceNoteSequentialEvent()

    def test_convert_with_attribute(self):
        after_grace_note_sequential_event = core_events.SequentialEvent(
            [music_events.NoteLike("c")]
        )
        self.assertEqual(
            self.converter(
                music_events.NoteLike(
                    after_grace_note_sequential_event=after_grace_note_sequential_event
                )
            ),
            after_grace_note_sequential_event,
        )


class MutwoParameterDictToNoteLikeTest(unittest.TestCase):
    def setUp(self):
        self.mutwo_parameter_dict_to_note_like = (
            music_converters.MutwoParameterDictToNoteLike()
        )

    def test_convert(self):
        playing_indicator_collection = (
            music_events.configurations.DEFAULT_PLAYING_INDICATORS_COLLECTION_CLASS()
        )
        playing_indicator_collection.articulation.name = "."
        notation_indicator_collection = (
            music_events.configurations.DEFAULT_NOTATION_INDICATORS_COLLECTION_CLASS()
        )
        notation_indicator_collection.clef.name = "treble"
        self.assertEqual(
            self.mutwo_parameter_dict_to_note_like.convert(
                {
                    "pitch_list": [music_parameters.DirectPitch(440)],
                    "duration": 10,
                    "volume": music_parameters.WesternVolume("f"),
                    "grace_note_sequential_event": core_events.SequentialEvent(
                        [music_events.NoteLike("f", 2, "pp")]
                    ),
                    "after_grace_note_sequential_event": core_events.SequentialEvent(
                        [music_events.NoteLike("g", 0.5, "f")]
                    ),
                    "playing_indicator_collection": playing_indicator_collection,
                    "notation_indicator_collection": notation_indicator_collection,
                }
            ),
            music_events.NoteLike(
                pitch_list=[music_parameters.DirectPitch(440)],
                duration=10,
                volume=music_parameters.WesternVolume("f"),
                grace_note_sequential_event=core_events.SequentialEvent(
                    [music_events.NoteLike("f", 2, "pp")]
                ),
                after_grace_note_sequential_event=core_events.SequentialEvent(
                    [music_events.NoteLike("g", 0.5, "f")]
                ),
                notation_indicator_collection=notation_indicator_collection,
                playing_indicator_collection=playing_indicator_collection,
            ),
        )


if __name__ == "__main__":
    unittest.main()
