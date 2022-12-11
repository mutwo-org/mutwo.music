"""Representations for musical instruments"""

import collections
import typing

import ranges

from mutwo import core_utilities
from mutwo import music_parameters


__all__ = (
    "UnpitchedInstrument",
    "ContinuousPitchedInstrument",
    "DiscreetPitchedInstrument",
    "Orchestration",
    "OrchestrationMixin",
)


class UnpitchedInstrument(music_parameters.abc.Instrument):
    """Modal a musical instruments without any clear pitches.

    **Example:**

    >>> from mutwo import music_parameters
    >>> bass_drum = music_parameters.UnpitchedInstrument("bass drum", "bd.")
    """

    @property
    def is_pitched(self) -> bool:
        return False


class ContinuousPitchedInstrument(music_parameters.abc.PitchedInstrument):
    """Modal a musical instrument with continuous pitches (e.g. not fretted).

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
        >>> music_parameters.WesternPitch('c', 1) in music_parameters.constants.BF_CLARINET
        False
        """
        return pitch in self.pitch_ambitus

    @property
    def pitch_ambitus(self) -> music_parameters.abc.PitchAmbitus:
        return self._pitch_ambitus


class DiscreetPitchedInstrument(music_parameters.abc.PitchedInstrument):
    """Modal a musical instrument with discreet pitches (e.g. fretted).

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
        ...   oboe0=music_parameters.constants.OBOE,
        ...   oboe1=music_parameters.constants.OBOE,
        ...   oboe2=music_parameters.constants.OBOE,
        ... )
        >>> orch.get_subset('oboe0', 'oboe2')
        Orchestration(oboe0=ContinuousPitchedInstrument(name='oboe', short_name='ob.', pitch_count_range=Range[1, 2), transposition_pitch_interval=DirectPitchInterval(interval = 0)), oboe2=ContinuousPitchedInstrument(name='oboe', short_name='ob.', pitch_count_range=Range[1, 2), transposition_pitch_interval=DirectPitchInterval(interval = 0)))
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
    ...   oboe0=music_parameters.constants.OBOE,
    ...   oboe1=music_parameters.constants.OBOE,
    ... )
    Orchestration(oboe0=ContinuousPitchedInstrument(name='oboe', short_name='ob.', pitch_count_range=Range[1, 2), transposition_pitch_interval=DirectPitchInterval(interval = 0)), oboe1=ContinuousPitchedInstrument(name='oboe', short_name='ob.', pitch_count_range=Range[1, 2), transposition_pitch_interval=DirectPitchInterval(interval = 0)))
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


# We add instruments to `music_parameters.constants`.


def instrument_name_to_variable_name(name: str) -> str:
    return name.upper().replace("-", "_")


def add_continuous_pitched_instruments():
    a, w, wi = (  # abbreviation for more compact code
        music_parameters.OctaveAmbitus,
        music_parameters.WesternPitch,
        music_parameters.WesternPitchInterval,
    )
    for name, short_name, ambitus, pitch_count_range, transposition_pitch_interval in (
        ("picollo", "pcl.", a(w("d", 5), w("c", 8)), (1, 2), wi("p-8")),
        ("flute", "flt.", a(w("c", 4), w("d", 7)), (1, 2), wi("p1")),
        ("oboe", "ob.", a(w("bf", 3), w("a", 6)), (1, 2), wi("p1")),
        ("bf-clarinet", "cl.", a(w("d", 3), w("bf", 6)), (1, 2), wi("m2")),
        ("ef-clarinet", "cl.", a(w("g", 3), w("ef", 7)), (1, 2), wi("m-3")),
        ("bassoon", "bs.", a(w("bf", 1), w("ef", 5)), (1, 2), wi("p1")),
    ):
        setattr(
            music_parameters.constants,
            instrument_name_to_variable_name(name),
            ContinuousPitchedInstrument(
                ambitus,
                name,
                short_name,
                ranges.Range(*pitch_count_range),
                transposition_pitch_interval,
            ),
        )


def add_instruments():
    add_continuous_pitched_instruments()


add_instruments()
# Cleanup
del add_instruments, add_continuous_pitched_instruments
