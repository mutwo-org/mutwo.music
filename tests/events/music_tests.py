import unittest

try:
    import quicktions as fractions  # type: ignore
except ImportError:
    import fractions  # type: ignore

from mutwo import core_events
from mutwo import music_events
from mutwo import music_parameters


class NoteLikeTest(unittest.TestCase):
    # ###################################################################### #
    #                          test pitch setter                             #
    # ###################################################################### #

    def test_pitch_list_setter_from_string(self):
        self.assertEqual(
            [music_parameters.WesternPitch("ds", octave=5)],
            music_events.NoteLike("ds5", 1, 1).pitch_list,
        )
        self.assertEqual(
            [music_parameters.WesternPitch("f")],
            music_events.NoteLike("f", 1, 1).pitch_list,
        )
        self.assertEqual(
            [
                music_parameters.WesternPitch("f"),
                music_parameters.WesternPitch("g", 2),
                music_parameters.WesternPitch("af"),
            ],
            music_events.NoteLike("f g2 af", 1, 1).pitch_list,
        )
        self.assertEqual(
            [music_parameters.JustIntonationPitch("3/2")],
            music_events.NoteLike("3/2", 1, 1).pitch_list,
        )
        self.assertEqual(
            [music_parameters.JustIntonationPitch("11/1")],
            music_events.NoteLike("11/1", 1, 1).pitch_list,
        )
        self.assertEqual(
            [
                music_parameters.JustIntonationPitch("5/3"),
                music_parameters.WesternPitch("aqs", 5),
            ],
            music_events.NoteLike("5/3 aqs5", 1, 1).pitch_list,
        )
        self.assertEqual([], music_events.NoteLike("", 1, 1).pitch_list)

    def test_pitch_list_setter_from_fraction(self):
        ratio = fractions.Fraction(3, 2)
        self.assertEqual(
            [music_parameters.JustIntonationPitch(ratio)],
            music_events.NoteLike(ratio, 1, 1).pitch_list,
        )

    def test_pitch_list_setter_from_None(self):
        self.assertEqual([], music_events.NoteLike(None, 1, 1).pitch_list)

    def test_pitch_list_setter_from_pitch(self):
        pitch_list = music_parameters.WesternPitch()
        self.assertEqual(
            [pitch_list], music_events.NoteLike(pitch_list, 1, 1).pitch_list
        )

    def test_pitch_list_setter_from_list(self):
        pitch_list = [
            music_parameters.WesternPitch(),
            music_parameters.JustIntonationPitch(),
        ]
        self.assertEqual(pitch_list, music_events.NoteLike(pitch_list, 1, 1).pitch_list)

    # ###################################################################### #
    #                          test volume setter                            #
    # ###################################################################### #

    def test_volume_setter_from_volume(self):
        volume = music_parameters.DirectVolume(-6)
        self.assertEqual(volume, music_events.NoteLike(None, 1, volume).volume)

    def test_volume_setter_from_number(self):
        volume = music_parameters.DirectVolume(-12)
        self.assertEqual(volume, music_events.NoteLike(None, 1, -12).volume)

    # ###################################################################### #
    #                   test grace notes setter                              #
    # ###################################################################### #

    def test_grace_note_consecution_setter_from_consecution(self):
        grace_note_consecution = core_events.Consecution(
            [music_events.NoteLike()]
        )
        self.assertEqual(
            grace_note_consecution,
            music_events.NoteLike(
                None, 1, 1, core_events.Consecution([]), grace_note_consecution
            ).after_grace_note_consecution,
        )

    # ###################################################################### #
    #                          test indicators setter                        #
    # ###################################################################### #

    def test_set_playing_indicator_collection(self):
        n = music_events.NoteLike(playing_indicator_collection="articulation.name=.")
        self.assertEqual(n.playing_indicator_collection.articulation.name, ".")
        n.playing_indicator_collection = "articulation.name = tenuto"
        self.assertEqual(n.playing_indicator_collection.articulation.name, "tenuto")

    def test_set_notation_indicator_collection(self):
        n = music_events.NoteLike(notation_indicator_collection="clef.name=bass")
        self.assertEqual(n.notation_indicator_collection.clef.name, "bass")
        n.notation_indicator_collection = "clef.name = treble_8"
        self.assertEqual(n.notation_indicator_collection.clef.name, "treble_8")

    # ###################################################################### #
    #                          other                                         #
    # ###################################################################### #

    def test_parameter_to_compare_tuple(self):
        note_like = music_events.NoteLike([music_parameters.WesternPitch()], 1, 1)
        expected_parameter_to_compare_tuple = (
            "after_grace_note_consecution",
            "duration",
            "grace_note_consecution",
            "instrument_list",
            "lyric",
            "notation_indicator_collection",
            "pitch_list",
            "playing_indicator_collection",
            "tag",
            "tempo",
            "volume",
        )
        self.assertEqual(
            note_like._parameter_to_compare_tuple, expected_parameter_to_compare_tuple
        )

    def test_equality_check(self):
        note_like0 = music_events.NoteLike([30], 1, 1)
        note_like1 = music_events.NoteLike([30], 1, 1)
        note_like2 = music_events.NoteLike([100], 1, 1)
        note_like3 = music_events.NoteLike([], 1, 2)
        note_like4 = music_events.NoteLike([400, 500], 1, 2)
        chronon = core_events.Chronon(1)

        self.assertEqual(note_like0, note_like0)
        self.assertEqual(note_like1, note_like0)
        self.assertEqual(note_like0, note_like1)  # different order

        self.assertNotEqual(note_like0, note_like2)
        self.assertNotEqual(note_like2, note_like0)  # different order
        self.assertNotEqual(note_like2, note_like3)
        self.assertNotEqual(note_like2, note_like4)
        self.assertNotEqual(note_like3, note_like4)
        self.assertNotEqual(note_like0, chronon)
        self.assertNotEqual(chronon, note_like0)  # different order
