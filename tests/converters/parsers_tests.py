import unittest

from mutwo import core_events
from mutwo import music_converters
from mutwo import music_events
from mutwo import music_parameters


class ChrononToPitchListTest(unittest.TestCase):
    def setUp(self):
        self.converter = music_converters.ChrononToPitchList()

    def test_convert_with_attribute(self):
        self.assertEqual(
            self.converter(music_events.NoteLike("1/1 3/2")),
            [
                music_parameters.JustIntonationPitch("1/1"),
                music_parameters.JustIntonationPitch("3/2"),
            ],
        )

    def test_convert_without_attribute(self):
        self.assertEqual(self.converter(core_events.Chronon(10)), [])


class ChrononToVolumeTest(unittest.TestCase):
    def setUp(self):
        self.converter = music_converters.ChrononToVolume()

    def test_convert_with_attribute(self):
        self.assertEqual(
            self.converter(music_events.NoteLike(volume="fff")),
            music_parameters.WesternVolume("fff"),
        )

    def test_convert_without_attribute(self):
        self.assertEqual(
            self.converter(core_events.Chronon(10)),
            music_parameters.AmplitudeVolume(0),
        )


class ChrononToInstrumentListTest(unittest.TestCase):
    def setUp(self):
        self.converter = music_converters.ChrononToInstrumentList()

    def test_convert_with_attribute(self):
        oboe = music_parameters.Oboe()
        self.assertEqual(
            self.converter(music_events.NoteLike(instrument_list=[oboe])), [oboe]
        )

    def test_convert_without_attribute(self):
        self.assertEqual(
            self.converter(core_events.Chronon(10)),
            [],
        )


class ChrononToPlayingIndicatorCollectionTest(unittest.TestCase):
    def setUp(self):
        self.converter = music_converters.ChrononToPlayingIndicatorCollection()

    def test_convert_with_attribute(self):
        self.assertEqual(
            self.converter(music_events.NoteLike()),
            music_events.configurations.DEFAULT_PLAYING_INDICATORS_COLLECTION_CLASS(),
        )

    def test_convert_without_attribute(self):
        self.assertEqual(
            self.converter(core_events.Chronon(10)),
            music_events.configurations.DEFAULT_PLAYING_INDICATORS_COLLECTION_CLASS(),
        )


class ChrononToNotationIndicatorCollectionTest(unittest.TestCase):
    def setUp(self):
        self.converter = music_converters.ChrononToNotationIndicatorCollection()

    def test_convert_with_attribute(self):
        self.assertEqual(
            self.converter(music_events.NoteLike()),
            music_events.configurations.DEFAULT_NOTATION_INDICATORS_COLLECTION_CLASS(),
        )

    def test_convert_without_attribute(self):
        self.assertEqual(
            self.converter(core_events.Chronon(10)),
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
        self.assertEqual(self.converter(core_events.Chronon(10)), "TEST")
        # Cleanup
        music_events.configurations.DEFAULT_NOTATION_INDICATORS_COLLECTION_CLASS = (
            default_notation_indicators_collection_class
        )


class ChrononToGraceOrAfterGraceNoteConsecutionTestMixin(object):
    def test_convert_without_attribute(self):
        self.assertEqual(
            self.converter(core_events.Chronon(10)),
            core_events.Consecution([]),
        )


class ChrononToGraceNoteConsecutionTest(
    unittest.TestCase, ChrononToGraceOrAfterGraceNoteConsecutionTestMixin
):
    def setUp(self):
        self.converter = music_converters.ChrononToGraceNoteConsecution()

    def test_convert_with_attribute(self):
        grace_note_consecution = core_events.Consecution(
            [music_events.NoteLike("c")]
        )
        self.assertEqual(
            self.converter(
                music_events.NoteLike(
                    grace_note_consecution=grace_note_consecution
                )
            ),
            grace_note_consecution,
        )

    def test_convert_without_attribute(self):
        self.assertEqual(
            self.converter(core_events.Chronon(10)),
            core_events.Consecution([]),
        )


class ChrononToAfterGraceNoteConsecutionTest(
    unittest.TestCase, ChrononToGraceOrAfterGraceNoteConsecutionTestMixin
):
    def setUp(self):
        self.converter = music_converters.ChrononToAfterGraceNoteConsecution()

    def test_convert_with_attribute(self):
        after_grace_note_consecution = core_events.Consecution(
            [music_events.NoteLike("c")]
        )
        self.assertEqual(
            self.converter(
                music_events.NoteLike(
                    after_grace_note_consecution=after_grace_note_consecution
                )
            ),
            after_grace_note_consecution,
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
                    "grace_note_consecution": core_events.Consecution(
                        [music_events.NoteLike("f", 2, "pp")]
                    ),
                    "after_grace_note_consecution": core_events.Consecution(
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
                grace_note_consecution=core_events.Consecution(
                    [music_events.NoteLike("f", 2, "pp")]
                ),
                after_grace_note_consecution=core_events.Consecution(
                    [music_events.NoteLike("g", 0.5, "f")]
                ),
                notation_indicator_collection=notation_indicator_collection,
                playing_indicator_collection=playing_indicator_collection,
            ),
        )


if __name__ == "__main__":
    unittest.main()
