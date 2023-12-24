import unittest

from mutwo import music_parameters
from mutwo import music_utilities

PC = music_parameters.PlayingIndicatorCollection
NC = music_parameters.NotationIndicatorCollection


class IndicatorCollectionParserTest(unittest.TestCase):
    def setUp(self):
        self.p = music_utilities.IndicatorCollectionParser()
        self.pc = PC()
        self.parse = lambda t: self.p.parse(t, self.pc)

    def test_parse_1string(self):
        self.assertEqual(self.pc.articulation.name, None)
        self.parse("articulation.name=stacatto")
        self.assertEqual(self.pc.articulation.name, "stacatto")

    def test_parse_1int(self):
        self.assertEqual(self.pc.tremolo.flag_count, None)
        self.parse("tremolo.flag_count=4")
        self.assertEqual(self.pc.tremolo.flag_count, 4)

    def test_parse_1float(self):
        self.assertEqual(self.pc.artifical_harmonic.semitone_count, None)
        self.parse("artifical_harmonic.semitone_count=2.5")
        self.assertEqual(self.pc.artifical_harmonic.semitone_count, 2.5)

    def test_parse_1bool(self):
        self.assertEqual(self.pc.hairpin.niente, False)
        self.parse("hairpin.niente=True")
        self.assertEqual(self.pc.hairpin.niente, True)
        self.parse("hairpin.niente=False")
        self.assertEqual(self.pc.hairpin.niente, False)

    def test_parse_1tuple(self):
        self.assertEqual(self.pc.woodwind_fingering.cc, None)
        self.parse("woodwind_fingering.cc=('a','b','c')")
        self.assertEqual(self.pc.woodwind_fingering.cc, ("a", "b", "c"))

    def test_parse1none(self):
        self.assertEqual(self.pc.pedal.activity, True)
        self.parse("pedal.activity")
        self.assertEqual(self.pc.pedal.activity, None)

    def test_parse_multiple(self):
        self._test_parse_multiple(
            "articulation.name=stacatto;pedal.activity;tremolo.flag_count=4"
        )

    def test_parse_multiple_with_whitespace(self):
        self._test_parse_multiple(
            "   pedal.activity; articulation.name=   stacatto  ;  tremolo.flag_count   =4"
        )

    def test_parse_multiple_with_newline(self):
        self._test_parse_multiple(
            "pedal.activity\narticulation.name=stacatto\n\ntremolo.flag_count=4"
        )

    def _test_parse_multiple(self, s: str):
        self.assertEqual(self.pc.articulation.name, None)
        self.assertEqual(self.pc.tremolo.flag_count, None)
        self.assertEqual(self.pc.pedal.activity, True)
        self.parse(s)
        self.assertEqual(self.pc.tremolo.flag_count, 4)
        self.assertEqual(self.pc.articulation.name, "stacatto")
        self.assertEqual(self.pc.pedal.activity, None)
