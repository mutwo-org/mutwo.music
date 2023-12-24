"""Define playing indicators for simple events.

This submodules provides several classes to add specific musical
playing techniques to :class:`mutwo.events.basic.SimpleEvent` objects.
They mostly derive from traditional Western playing techniques and their
notation. Unlike indicators of the :mod:`mutwo.music_parameters.notation_indicators`
module, playing indicators have an effect on the played music and aren't
merely specifications of representation. The proper way to handle
playing  indicators should be via a :class:`PlayingIndicatorCollection`
object that should be attached to the respective :class:`SimpleEvent`.
The collection contains all possible playing indicators which are defined
in this module. :class:`mutwo.events.music.NoteLike` contain by default
a playing indicator collection.

There are basically two different types of playing indicators:

1, Playing indicators which can only be on or off (for instance
``bartok_pizzicato``, ``prall`` or ``laissez_vibrer``). They have
a :attr:`is_active` attribute which can either be :obj:`True`
or :obj:`False`.

2. Playing indicators with one or more arguments (for instance
:class:`Tremolo` with :attr:`flag_count` or :class:`Arpeggio` with
:attr:`direction`). Their :attr:`is_active` attribute can't be
set by the user and get automatically initialised depending on
if all necessary attributes are defined (then active) or
if any of the necessary attributes is set to :obj:`None` (then
not active).

**Example:**

Set playing indicators of :class:`NoteLike`:

>>> from mutwo import music_events
>>> my_note = music_events.NoteLike('c', 1 / 4, 'mf')
>>> my_note.playing_indicator_collection.articulation.name = "."  # add staccato
>>> my_chord = music_events.NoteLike('c e g', 1 / 2, 'f')
>>> my_chord.playing_indicator_collection.arpeggio.direction= "up"  # add arpeggio
>>> my_chord.playing_indicator_collection.laissez_vibrer = True  # and laissez_vibrer

Attach :class:`PlayingIndicatorCollection` to :class:`SimpleEvent`:

>>> from mutwo import core_events
>>> from mutwo import music_parameters
>>> my_simple_event = core_events.SimpleEvent(1)
>>> my_simple_event.playing_indicator_collection = music_parameters.PlayingIndicatorCollection()
"""

import dataclasses
import inspect
import typing

from mutwo import music_parameters


@dataclasses.dataclass()
class Tremolo(music_parameters.abc.ImplicitPlayingIndicator):
    flag_count: typing.Optional[int] = None


@dataclasses.dataclass()
class Articulation(music_parameters.abc.ImplicitPlayingIndicator):
    name: typing.Optional[music_parameters.constants.ARTICULATION_LITERAL] = None


@dataclasses.dataclass()
class Arpeggio(music_parameters.abc.ImplicitPlayingIndicator):
    direction: typing.Optional[music_parameters.constants.DIRECTION_LITERAL] = None


@dataclasses.dataclass()
class Pedal(music_parameters.abc.ImplicitPlayingIndicator):
    type: typing.Optional[music_parameters.constants.PEDAL_TYPE_LITERAL] = None
    activity: typing.Optional[bool] = True


@dataclasses.dataclass()
class Slur(music_parameters.abc.ImplicitPlayingIndicator):
    activity: typing.Optional[bool] = None


@dataclasses.dataclass()
class StringContactPoint(music_parameters.abc.ImplicitPlayingIndicator):
    contact_point: typing.Optional[
        music_parameters.constants.CONTACT_POINT_LITERAL
    ] = None


@dataclasses.dataclass()
class Ornamentation(music_parameters.abc.ImplicitPlayingIndicator):
    direction: typing.Optional[music_parameters.constants.DIRECTION_LITERAL] = None
    count: int = 1


@dataclasses.dataclass()
class BendAfter(music_parameters.abc.ImplicitPlayingIndicator):
    # Content music_parameters
    bend_amount: typing.Optional[float] = None
    # Presentation music_parameters
    minimum_length: typing.Optional[float] = 3
    thickness: typing.Optional[float] = 3


@dataclasses.dataclass()
class ArtificalHarmonic(music_parameters.abc.ImplicitPlayingIndicator):
    semitone_count: typing.Optional[int] = None


class NaturalHarmonicNodeList(
    list[music_parameters.NaturalHarmonic.Node], music_parameters.abc.PlayingIndicator
):
    """Assign natural harmonics to your note.

    **Example:**

    >>> from mutwo import music_events, music_parameters
    >>> n = music_events.NoteLike('c', 4)
    >>> n.playing_indicator_collection.natural_harmonic_node_list.is_active
    False
    >>> n.playing_indicator_collection.natural_harmonic_node_list.append(
    ...     music_parameters.NaturalHarmonic(
    ...         2,
    ...         music_parameters.String(0, music_parameters.WesternPitch('c', 3))
    ...     ).node_tuple[0]
    ... )
    >>> n.playing_indicator_collection.natural_harmonic_node_list.is_active
    True
    """

    def __new__(
        self,
        natural_harmonic_list: typing.Optional[
            list[music_parameters.NaturalHarmonic.Node]
        ] = None,
        harmonic_note_head_style: bool = True,
        write_string: bool = True,
        parenthesize_lower_note_head: bool = False,
    ):
        nhn_list = super().__new__(self, natural_harmonic_list or [])
        nhn_list.write_string = write_string
        nhn_list.harmonic_note_head_style = harmonic_note_head_style
        nhn_list.parenthesize_lower_note_head = parenthesize_lower_note_head
        return nhn_list

    @property
    def is_active(self) -> bool:
        return bool(self)


@dataclasses.dataclass()
class Fermata(music_parameters.abc.ImplicitPlayingIndicator):
    type: typing.Optional[music_parameters.constants.FERMATA_TYPE_LITERAL] = None


@dataclasses.dataclass()
class Hairpin(music_parameters.abc.ImplicitPlayingIndicator):
    symbol: typing.Optional[music_parameters.constants.HAIRPIN_SYMBOL_LITERAL] = None
    niente: bool = False


@dataclasses.dataclass()
class Trill(music_parameters.abc.ImplicitPlayingIndicator):
    pitch: typing.Optional[music_parameters.abc.Pitch] = None


@dataclasses.dataclass()
class WoodwindFingering(music_parameters.abc.ImplicitPlayingIndicator):
    cc: typing.Optional[typing.Tuple[str, ...]] = None
    left_hand: typing.Optional[typing.Tuple[str, ...]] = None
    right_hand: typing.Optional[typing.Tuple[str, ...]] = None
    instrument: str = "clarinet"


@dataclasses.dataclass()
class Cue(music_parameters.abc.ImplicitPlayingIndicator):
    """Cue for electronics etc."""

    index: typing.Optional[int] = None


def f(factory=music_parameters.abc.ExplicitPlayingIndicator):
    return dataclasses.field(default_factory=factory)


@dataclasses.dataclass
class PlayingIndicatorCollection(
    music_parameters.abc.IndicatorCollection[music_parameters.abc.PlayingIndicator]
):
    articulation: Articulation = f(Articulation)
    artifical_harmonic: ArtificalHarmonic = f(ArtificalHarmonic)
    arpeggio: Arpeggio = f(Arpeggio)
    bartok_pizzicato: music_parameters.abc.PlayingIndicator = f()
    bend_after: BendAfter = f(BendAfter)
    breath_mark: music_parameters.abc.PlayingIndicator = f()
    cue: Cue = f(Cue)
    duration_line_dashed: music_parameters.abc.PlayingIndicator = f()
    duration_line_triller: music_parameters.abc.PlayingIndicator = f()
    fermata: Fermata = f(Fermata)
    glissando: music_parameters.abc.PlayingIndicator = f()
    hairpin: Hairpin = f(Hairpin)
    natural_harmonic_node_list: NaturalHarmonicNodeList = f(NaturalHarmonicNodeList)
    laissez_vibrer: music_parameters.abc.PlayingIndicator = f()
    optional: music_parameters.abc.PlayingIndicator = f()
    ornamentation: Ornamentation = f(Ornamentation)
    pedal: Pedal = f(Pedal)
    prall: music_parameters.abc.PlayingIndicator = f()
    slur: Slur = f(Slur)
    string_contact_point: StringContactPoint = f(StringContactPoint)
    tie: music_parameters.abc.PlayingIndicator = f()
    tremolo: Tremolo = f(Tremolo)
    trill: Trill = f(Trill)
    woodwind_fingering: WoodwindFingering = f(WoodwindFingering)

    def __setattr__(self, parameter_name: str, value: bool):
        """Overriding default behaviour to allow syntactic sugar.

        This method allows syntax like:

            playing_indicator_collection.tie = True

        which is the same as

            playing_indicator_collection.tie.is_active = True

        Furthermore the methods makes sure that no property
        can actually be overridden.
        """

        if (playing_indicator := getattr(self, parameter_name, None)) is not None:
            if isinstance(
                playing_indicator, music_parameters.abc.ExplicitPlayingIndicator
            ):
                playing_indicator.is_active = bool(value)
            else:
                raise dataclasses.FrozenInstanceError(
                    "Can't override frozen property (playing indicator)"
                    f" '{playing_indicator}'!"
                )
        else:
            super().__setattr__(parameter_name, value)


# Dynamically define __all__ in order to catch all PlayingIndicator classes
__all__ = tuple(
    name
    for name, cls in globals().items()
    if inspect.isclass(cls)
    and music_parameters.abc.PlayingIndicator in inspect.getmro(cls)
) + ("PlayingIndicatorCollection",)
