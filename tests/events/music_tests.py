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
        volume = music_parameters.DecibelVolume(-6)
        self.assertEqual(volume, music_events.NoteLike(None, 1, volume).volume)

    def test_volume_setter_from_positive_number(self):
        amplitude = 0.5
        volume = music_parameters.DirectVolume(amplitude)
        self.assertEqual(volume, music_events.NoteLike(None, 1, amplitude).volume)

    def test_volume_setter_from_negative_number(self):
        n_decibel = -12
        volume = music_parameters.DecibelVolume(n_decibel)
        self.assertEqual(volume, music_events.NoteLike(None, 1, n_decibel).volume)

    # ###################################################################### #
    #                   test grace notes setter                              #
    # ###################################################################### #

    def test_grace_note_sequential_event_setter_from_simple_event(self):
        grace_note_sequential_event = music_events.NoteLike()
        self.assertEqual(
            core_events.SequentialEvent([grace_note_sequential_event]),
            music_events.NoteLike(
                None, 1, 1, grace_note_sequential_event
            ).grace_note_sequential_event,
        )

    def test_grace_note_sequential_event_setter_from_sequential_event(self):
        grace_note_sequential_event = core_events.SequentialEvent(
            [music_events.NoteLike()]
        )
        self.assertEqual(
            grace_note_sequential_event,
            music_events.NoteLike(
                None, 1, 1, core_events.SequentialEvent([]), grace_note_sequential_event
            ).after_grace_note_sequential_event,
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
            "after_grace_note_sequential_event",
            "duration",
            "grace_note_sequential_event",
            "instrument_list",
            "lyric",
            "notation_indicator_collection",
            "pitch_list",
            "playing_indicator_collection",
            "tempo_envelope",
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
        simple_event = core_events.SimpleEvent(1)

        self.assertEqual(note_like0, note_like0)
        self.assertEqual(note_like1, note_like0)
        self.assertEqual(note_like0, note_like1)  # different order

        self.assertNotEqual(note_like0, note_like2)
        self.assertNotEqual(note_like2, note_like0)  # different order
        self.assertNotEqual(note_like2, note_like3)
        self.assertNotEqual(note_like2, note_like4)
        self.assertNotEqual(note_like3, note_like4)
        self.assertNotEqual(note_like0, simple_event)
        self.assertNotEqual(simple_event, note_like0)  # different order
