from __future__ import annotations

import collections
import dataclasses
import functools
import typing

import quicktions as fractions

from mutwo import core_utilities
from mutwo import music_parameters


__all__ = (
    "NaturalHarmonic",
    "String",
    "UnpitchedInstrument",
    "ContinuousPitchedInstrument",
    "DiscreetPitchedInstrument",
    "ContinuousPitchedStringInstrument",
    "DiscreetPitchedStringInstrument",
    "Orchestration",
    "OrchestrationMixin",
)


class NaturalHarmonic(music_parameters.Partial):
    """Model the natural harmonic of a :class:`String`.

    :param index: The partials index.
    :type index: int
    :param string: The :class:`String` on which this harmonic
        shall be played.
    :type string: String
    """

    @dataclasses.dataclass(frozen=True)
    class Node(object):
        """A position on a string which, if touched, produces a harmonic.

        :param interval: The `interval` remarks the position on the string
            where the player needs to press in order to produce a harmonic.
            The interval needs to be added to the :class:`String` tuning
            in order to gain a pitch. The position where this pitch is played
            normally on the given string is the node position where the
            harmonic can be produced.
        :type interval: music_parameters.abc.PitchInterval
        :param string: The string on which to play the node,
        :type string: String
        """

        interval: music_parameters.abc.PitchInterval
        string: String

        @functools.cached_property
        def pitch(self) -> music_parameters.abc.Pitch:
            """At which position to press the string to produce harmonic."""
            return self.string.tuning_original + self.interval

    def __init__(self, index: int, string: String):
        self._string = string
        super().__init__(index, tonality=True)  # We can't play undertones

    @property
    def string(self) -> String:
        """The :class:`String` on which the harmonic is played."""
        return self._string

    @functools.cached_property
    def pitch(self) -> music_parameters.JustIntonationPitch:
        """The resulting sounding pitch of a :class:`NaturalHarmonic`.

        **Example:**

        >>> from mutwo import music_parameters
        >>> string = music_parameters.String(music_parameters.WesternPitch("g", 3))
        >>> natural_harmonic = music_parameters.NaturalHarmonic(3, string)
        >>> natural_harmonic.pitch
        WesternPitch('d', 5)
        """
        return self.string.tuning + self.interval

    @functools.cached_property
    def node_tuple(self) -> tuple[NaturalHarmonic.Node, ...]:
        """Find all :class:`NaturalHarmonic.Node` on which harmonic is playable.

        **Example:**

        >>> from mutwo import music_parameters
        >>> natural_harmonic = music_parameters.NaturalHarmonic(
        ...     2,
        ...     music_parameters.String(music_parameters.WesternPitch('g', 3)),
        ... )
        (NaturalHarmonic.Node(interval=JustIntonationPitch('3/2'), string=String(WesternPitch('g', 3))), NaturalHarmonic.Node(interval=JustIntonationPitch('3/1'), string=String(WesternPitch('g', 3))))
        """
        node_list = []
        for node_index in range(1, self.index):
            ratio = fractions.Fraction(self.index, node_index)
            if ratio.numerator == self.index:
                node_list.append(
                    self.Node(music_parameters.JustIntonationPitch(ratio), self.string)
                )
        return tuple(reversed(node_list))


@dataclasses.dataclass(frozen=True)
class String(object):
    """:class:`String` represents a string of an instrument.

    :param tuning: The pitch to which the string is tuned to.
    :type tuning: music_parameters.abc.Pitch
    :param tuning_original: If the standard tuning of a string
        differs from its current tuning (e.g. if a scordatura
        is used) this parameter can be set to the standard tuning.
        This is useful in case one wants to notate the fingering
        of a harmonic and not the sounding result. The ``pitch``
        attribute of :class:`NaturalHarmonic.Node` uses `tuning_original`
        for calculation instead of `tuning. If `tuning_original`
        is ``None`` it is auto-set to `tuning`. Default to ``None``.
    :type tuning_original: typing.Optional[music_parameters.abc.Pitch]
    :param max_natural_harmonic_index: Although we can imagine infinite
        number of natural harmonics, in the real world it's not so
        easy to play higher flageolet. It's therefore a good idea
        to denote a limit of the highest natural harmonic. This
        limit defines the highest :class:`NaturalHarmonic` which is
        returned when accessing :class:`String`s
        ``natural_harmonic_tuple`` property. No matter what is
        set to ``max_natural_harmonic_index``, you can still get
        infinitely high :class:`NaturalHarmonic` of a :class:`String`
        with its ``index_to_natural_harmonic`` method. Default to 6.
    :type max_natural_harmonic_index: int

    **Example:**

    >>> from mutwo import music_parameters
    >>> g_string = music_parameters.String(music_parameters.WesternPitch('g', 3))
    >>> g_string
    String(WesternPitch('g', 3))
    >>> retuned_g_string = music_parameters.String(
    ...     music_parameters.WesternPitch('g', 3),
    ...     tuning_original=music_parameters.JustIntonationPitch('8/11'),
    ... )
    >>> retuned_g_string
    String(WesternPitch('g', 3))
    """

    tuning: music_parameters.abc.Pitch
    tuning_original: typing.Optional[music_parameters.abc.Pitch] = None
    max_natural_harmonic_index: int = 6

    def __post_init__(self):
        object.__setattr__(self, "tuning_original", self.tuning_original or self.tuning)
        object.__setattr__(self, "_index_to_natural_harmonic", {})

    def __repr__(self) -> str:
        return f"{type(self).__name__}({self.tuning})"

    @functools.cached_property
    def natural_harmonic_tuple(self) -> tuple[NaturalHarmonic, ...]:
        """All :class:`NaturalHarmonic` with index from 2 until ``max_natural_harmonic_index``."""
        return tuple(
            (
                self.index_to_natural_harmonic(i)
                for i in range(2, self.max_natural_harmonic_index + 1)
            )
        )

    def index_to_natural_harmonic(self, natural_harmonic_index: int) -> NaturalHarmonic:
        """Find natural harmonic with given partial index.

        :param natural_harmonic_index: The partial index; e.g. 2 is the first
            overtone (an octave above the root), 3 the second overtone (octave
            plus fifth), etc.
        :type natural_harmonic_index: int

        **Example:**

        >>> from mutwo import music_parameters
        >>> g_string = music_parameters.String(
        ...     music_parameters.WesternPitch('g', 3)
        ... )
        >>> g_string.index_to_natural_harmonic(5)
        NaturalHarmonic(index=5, tonality=True)
        """
        try:
            return self._index_to_natural_harmonic[natural_harmonic_index]
        except KeyError:
            h = self._index_to_natural_harmonic[
                natural_harmonic_index
            ] = NaturalHarmonic(natural_harmonic_index, self)
            return h


@dataclasses.dataclass(frozen=True)
class StringInstrumentMixin(object):
    """Mixin to model instrument with strings.

    :param string_tuple: All strings which the instrument has.
    :type string_tuple: tuple[String, ...]

    This class provides additional attributes and methods for
    an instrument with strings.

    The class itself is not an :class:`Instrument`, but only a mixin.
    In order to use it with an :class:`Instrument`, you need to
    inherit from both and explicitly call '__init__' of both
    super classes inside your '__init__' method.

    It's recommended to simply use builtin :class:`ContinuousPitchedStringInstrument`
    or :class:`DiscreetPitchedStringInstrument`.

    Harmonic pitches have no effect on the `__contains__`
    method of an `Instrument`. This means the expression

        ``pitch in instrument``

    ignores all pitches returned by the `harmonic_pitch_tuple`
    property. This is because it is assumed that the user needs
    an explicit additional test to check if a pitch can be played
    by harmonics (because often we may find ourselves in a situation
    where we don't want a harmonic).
    """

    string_tuple: tuple[String, ...]

    @functools.cached_property
    def harmonic_pitch_tuple(self) -> tuple[music_parameters.abc.Pitch, ...]:
        """List all pitches which can be played with natural harmonics.

        This tuple depends on ``max_natural_harmonic_index`` attribute of
        :class:`String`.
        """
        pitch_list = []
        for s in self.string_tuple:
            for h in s.natural_harmonic_tuple:
                if (p := h.pitch) not in pitch_list:
                    pitch_list.append(p)
        return tuple(sorted(pitch_list))

    @functools.cached_property
    def harmonic_pitch_ambitus(self) -> music_parameters.abc.PitchAmbitus:
        """Get flageolet :class:`music_parameters.abc.PitchAmbitus`."""
        hp_tuple = self.harmonic_pitch_tuple
        return music_parameters.OctaveAmbitus(hp_tuple[0], hp_tuple[1])

    def get_harmonic_pitch_variant_tuple(
        self,
        pitch: music_parameters.abc.Pitch,
        period: typing.Optional[music_parameters.abc.PitchInterval] = None,
        tolerance: music_parameters.abc.PitchInterval = music_parameters.DirectPitchInterval(
            2
        ),
    ) -> tuple[music_parameters.abc.Pitch, ...]:
        """Find natural harmonic pitch variants (in all registers) of ``pitch``

        :param pitch: The pitch which variants shall be found.
        :type pitch: music_parameters.abc.Pitch
        :param period: The repeating period (usually an octave). If the
            period is set to `None` the function will fallback to them
            objects method :method:`pitch_to_period`. Default to `None`.
        :type period: typing.Optional[music_parameters.abc.PitchInterval]
        :param tolerance: Because harmonics are just tuned they may
            differ from tempered pitches. In order to still fetch harmonics
            the ``tolerance`` parameter can help. This is a
            :class:`music_parameters.abc.PitchInterval`: if the difference
            is within the intervals range, it is still considered as equal
            and the harmonic is returned. Default to `DirectPitchInterval`
            with 2 cents.
        :type tolerance: music_parameters.abc.PitchInterval
        """
        t_interval = abs(tolerance.interval)
        g = self.harmonic_pitch_ambitus.get_pitch_variant_tuple
        h_t = self.harmonic_pitch_tuple
        return tuple(
            p
            for p in g(pitch, period)
            if any(
                [abs(p.get_pitch_interval(h_p).interval) < t_interval for h_p in h_t]
            )
        )

    def pitch_to_natural_harmonic_tuple(
        self,
        pitch: music_parameters.abc.Pitch,
        tolerance: music_parameters.abc.PitchInterval = music_parameters.DirectPitchInterval(
            2
        ),
    ) -> tuple[NaturalHarmonic, ...]:
        """Find all :class:`NaturalHarmonic` which produces ``pitch``.

        :param pitch: The pitch which shall be equal to the returned
            harmonics pitch.
        :type pitch: music_parameters.abc.Pitch
        :param tolerance: Because harmonics are just tuned they may
            differ from tempered pitches. In order to still fetch harmonics
            the ``tolerance`` parameter can help. This is a
            :class:`music_parameters.abc.PitchInterval`: if the difference
            is within the intervals range, it is still considered as equal
            and the harmonic is returned. Default to `DirectPitchInterval`
            with 2 cents.
        :type tolerance: music_parameters.abc.PitchInterval
        """
        t_interval = abs(tolerance.interval)
        natural_harmonic_list = []
        for s in self.string_tuple:
            for h in s.natural_harmonic_tuple:
                if abs((h.pitch.get_pitch_interval(pitch)).interval) < t_interval:
                    natural_harmonic_list.append(h)
        return tuple(natural_harmonic_list)


class UnpitchedInstrument(music_parameters.abc.Instrument):
    """Model a musical instruments without any clear pitches.

    **Example:**

    >>> from mutwo import music_parameters
    >>> bass_drum = music_parameters.UnpitchedInstrument("bass drum", "bd.")
    """

    @property
    def is_pitched(self) -> bool:
        return False


class ContinuousPitchedInstrument(music_parameters.abc.PitchedInstrument):
    """Model a musical instrument with continuous pitches (e.g. not fretted).

    :param pitch_ambitus: The pitch ambitus of the instrument.
    :type pitch_ambitus: music_parameters.abc.PitchAmbitus
    :param name: The name of the instrument.
    :type name: str
    :param short_name: The abbreviation of the instrument.
        If set to ``None`` it will be the same like `name`.
        Default to ``None``.
    :type short_name: typing.Optional[str]
    :param pitch_count_range: Set how many simultaneous
        pitches the instrument can play. Default to
        `ranges.Range(1, 2)`, which means that the instrument
        is monophonic.
    :type pitch_count_range: ranges.Range
    :param transposition_pitch_interval: Some instruments are
        written with a transposition (so sounding pitch and
        written pitch differs). This parameter can be used
        to set the transposition interval in case sounding
        and written differs. The `transposition_pitch_interval`
        is added to the sounding pitches in order to reach the
        written pitches. If set to ``None`` this will be
        set to `DirectPitchInterval(0)` which is no transposition.
        Default to ``None``.
    :type transposition_pitch_interval: typing.Optional[PitchInterval]

    **Example:**

    >>> from mutwo import music_parameters
    >>> vl = music_parameters.ContinuousPitchedInstrument(
    ...     music_parameters.OctaveAmbitus(
    ...         music_parameters.WesternPitch('g', 3),
    ...         music_parameters.WesternPitch('e', 7),
    ...     ),
    ...     "violin",
    ...     "vl.",
    ... )
    """

    def __init__(
        self, pitch_ambitus: music_parameters.abc.PitchAmbitus, *args, **kwargs
    ):
        super().__init__(*args, **kwargs)
        self._pitch_ambitus = pitch_ambitus

    def __contains__(self, pitch: typing.Any) -> bool:
        """Test if pitch is playable by instrument.

        :param pitch: Pitch to test.
        :type pitch: typing.Any

        **Example:**

        >>> from mutwo import music_parameters
        >>> music_parameters.WesternPitch('c', 1) in music_parameters.BfClarinet()
        False
        """
        return pitch in self.pitch_ambitus

    @property
    def pitch_ambitus(self) -> music_parameters.abc.PitchAmbitus:
        return self._pitch_ambitus

    def get_pitch_variant_tuple(
        self,
        pitch: music_parameters.abc.Pitch,
        period: typing.Optional[music_parameters.abc.PitchInterval] = None,
    ) -> tuple[music_parameters.abc.Pitch, ...]:
        return self.pitch_ambitus.get_pitch_variant_tuple(pitch, period)


class DiscreetPitchedInstrument(music_parameters.abc.PitchedInstrument):
    """Model a musical instrument with discreet pitches (e.g. fretted).

    :param pitch_tuple: A tuple of all playable pitches of the instrument.
    :type pitch_tuple: tuple[music_parameters.abc.Pitch, ...]
    :param name: The name of the instrument.
    :type name: str
    :param short_name: The abbreviation of the instrument.
        If set to ``None`` it will be the same like `name`.
        Default to ``None``.
    :type short_name: typing.Optional[str]
    :param pitch_count_range: Set how many simultaneous
        pitches the instrument can play. Default to
        `ranges.Range(1, 2)`, which means that the instrument
        is monophonic.
    :type pitch_count_range: ranges.Range
    :param transposition_pitch_interval: Some instruments are
        written with a transposition (so sounding pitch and
        written pitch differs). This parameter can be used
        to set the transposition interval in case sounding
        and written differs. The `transposition_pitch_interval`
        is added to the sounding pitches in order to reach the
        written pitches. If set to ``None`` this will be
        set to `DirectPitchInterval(0)` which is no transposition.
        Default to ``None``.
    :type transposition_pitch_interval: typing.Optional[PitchInterval]

    **Example:**

    >>> from mutwo import music_parameters
    >>> pentatonic_idiophone = music_parameters.DiscreetPitchedInstrument(
    ...     (
    ...         music_parameters.JustIntonationPitch('1/1'),
    ...         music_parameters.JustIntonationPitch('9/8'),
    ...         music_parameters.JustIntonationPitch('5/4'),
    ...         music_parameters.JustIntonationPitch('3/2'),
    ...         music_parameters.JustIntonationPitch('7/4'),
    ...     ),
    ...     "idiophone",
    ...     "id.",
    ... )
    """

    def __init__(
        self, pitch_tuple: tuple[music_parameters.abc.Pitch, ...], *args, **kwargs
    ):
        super().__init__(*args, **kwargs)
        self._pitch_tuple = tuple(sorted(core_utilities.uniqify_sequence(pitch_tuple)))
        self._pitch_ambitus = music_parameters.OctaveAmbitus(
            pitch_tuple[0], pitch_tuple[-1]
        )

    def __contains__(self, pitch: typing.Any) -> bool:
        return pitch in self.pitch_tuple

    @property
    def pitch_ambitus(self) -> music_parameters.abc.PitchAmbitus:
        return self._pitch_ambitus

    @property
    def pitch_tuple(self) -> tuple[music_parameters.abc.Pitch, ...]:
        return self._pitch_tuple

    def get_pitch_variant_tuple(
        self,
        pitch: music_parameters.abc.Pitch,
        period: typing.Optional[music_parameters.abc.PitchInterval] = None,
    ) -> tuple[music_parameters.abc.Pitch, ...]:
        return tuple(
            filter(
                lambda p: p in self.pitch_tuple,
                self.pitch_ambitus.get_pitch_variant_tuple(pitch, period),
            )
        )


class ContinuousPitchedStringInstrument(
    ContinuousPitchedInstrument, StringInstrumentMixin
):
    def __init__(self, *args, string_tuple: tuple[String, ...], **kwargs):
        ContinuousPitchedInstrument.__init__(self, *args, **kwargs)
        StringInstrumentMixin.__init__(self, string_tuple)


class DiscreetPitchedStringInstrument(DiscreetPitchedInstrument, StringInstrumentMixin):
    def __init__(self, *args, string_tuple: tuple[String, ...], **kwargs):
        DiscreetPitchedInstrument.__init__(self, *args, **kwargs)
        StringInstrumentMixin.__init__(self, string_tuple)


class OrchestrationMixin(object):
    """Helper base class from which adhoc created `Orchestration` object inherits.

    This class has some methods which extend the functionality of
    Pythons builtin `collections.namedtuple`.
    """

    def get_subset(self, *instrument_name: str):
        r"""Return a sub-Orchestration of `Orchestration`.

        :param \*instrument_name: Name of the instrument which should be
            included in the subset.
        :type \*instrument_name: str

        This method doesn't change the original `Orchestration`
        but creates a new object.

        **Example:**

        >>> from mutwo import music_parameters
        >>> orch = music_parameters.Orchestration(
        ...   oboe0=music_parameters.Oboe(),
        ...   oboe1=music_parameters.Oboe(),
        ...   oboe2=music_parameters.Oboe(),
        ... )
        >>> orch.get_subset('oboe0', 'oboe2')
        Orchestration(oboe0=Oboe(name='oboe', short_name='ob.', pitch_count_range=Range[1, 2), transposition_pitch_interval=DirectPitchInterval(interval = 0)), oboe2=Oboe(name='oboe', short_name='ob.', pitch_count_range=Range[1, 2), transposition_pitch_interval=DirectPitchInterval(interval = 0)))
        """
        return Orchestration(**{name: getattr(self, name) for name in instrument_name})


def Orchestration(**instrument_name_to_instrument: music_parameters.abc.Instrument):
    r"""Create a name space for the instrumentation of a composition.

    :param \**instrument_name_to_instrument: Pick any instrument name
        and map it to a specific instrument.
    :type \**instrument_name_to_instrument: music_parameters.abc.Instrument

    This returns an adapted `namedtuple instance <https://docs.python.org/3/library/collections.html#collections.namedtuple>`_
    where the keys are the instrument names and the values are the
    :class:`mutwo.music_parameters.abc.Instrument` objects.
    The returned `Orchestration` object has some additional methods.
    They are documented in the :class`OrchestrationMixin`.

    **Example:**

    >>> from mutwo import music_parameters
    >>> music_parameters.Orchestration(
    ...   oboe0=music_parameters.Oboe(),
    ...   oboe1=music_parameters.Oboe(),
    ... )
    Orchestration(oboe0=Oboe(name='oboe', short_name='ob.', pitch_count_range=Range[1, 2), transposition_pitch_interval=DirectPitchInterval(interval = 0)), oboe1=Oboe(name='oboe', short_name='ob.', pitch_count_range=Range[1, 2), transposition_pitch_interval=DirectPitchInterval(interval = 0)))
    """

    instrument_name_tuple, instrument_tuple = zip(
        *instrument_name_to_instrument.items()
    )

    return type(
        "Orchestration",
        (
            collections.namedtuple("Orchestration", instrument_name_tuple),
            OrchestrationMixin,
        ),
        {},
    )(*instrument_tuple)


# Helper
def _setdefault(kwargs: dict, default_dict: dict) -> dict:
    for key, value in default_dict.items():
        kwargs.setdefault(key, value)
    return kwargs
