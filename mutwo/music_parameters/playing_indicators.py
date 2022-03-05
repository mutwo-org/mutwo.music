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
:class:`Tremolo` with :attr:`n_flags` or :class:`Arpeggio` with
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
>>> my_chord = music.NoteLike('c e g', 1 / 2, 'f')
>>> my_chord.playing_indicator_collection.arpeggio.direction= "up"  # add arpeggio
>>> my_chord.playing_indicator_collection.laissez_vibrer = True  # and laissez_vibrer

Attach :class:`PlayingIndicatorCollection` to :class:`SimpleEvent`:

>>> from mutwo import core_events
>>> from mutwo import music_parameters
>>> my_simple_event = core_events.SimpleEvent()
>>> my_simple_event.playing_indicator_collection = music_parameters.PlayingIndicatorCollection()
"""

import dataclasses
import inspect
import typing

from mutwo import music_parameters


@dataclasses.dataclass()
class Tremolo(music_parameters.abc.ImplicitPlayingIndicator):
    n_flags: typing.Optional[int] = None


@dataclasses.dataclass()
class Articulation(music_parameters.abc.ImplicitPlayingIndicator):
    name: typing.Optional[music_parameters.constants.ARTICULATION_LITERAL] = None


@dataclasses.dataclass()
class Arpeggio(music_parameters.abc.ImplicitPlayingIndicator):
    direction: typing.Optional[music_parameters.constants.DIRECTION_LITERAL] = None


@dataclasses.dataclass()
class Pedal(music_parameters.abc.ImplicitPlayingIndicator):
    pedal_type: typing.Optional[music_parameters.constants.PEDAL_TYPE_LITERAL] = None
    pedal_activity: typing.Optional[bool] = True


@dataclasses.dataclass()
class StringContactPoint(music_parameters.abc.ImplicitPlayingIndicator):
    contact_point: typing.Optional[
        music_parameters.constants.CONTACT_POINT_LITERAL
    ] = None


@dataclasses.dataclass()
class Ornamentation(music_parameters.abc.ImplicitPlayingIndicator):
    direction: typing.Optional[music_parameters.constants.DIRECTION_LITERAL] = None
    n_times: int = 1


@dataclasses.dataclass()
class BendAfter(music_parameters.abc.ImplicitPlayingIndicator):
    # Content music_parameters
    bend_amount: typing.Optional[float] = None
    # Presentation music_parameters
    minimum_length: typing.Optional[float] = 3
    thickness: typing.Optional[float] = 3


@dataclasses.dataclass()
class ArtificalHarmonic(music_parameters.abc.ImplicitPlayingIndicator):
    n_semitones: typing.Optional[int] = None


@dataclasses.dataclass()
class PreciseNaturalHarmonic(music_parameters.abc.ImplicitPlayingIndicator):
    string_pitch: typing.Optional[music_parameters.WesternPitch] = None
    played_pitch: typing.Optional[music_parameters.WesternPitch] = None
    harmonic_note_head_style: bool = True
    parenthesize_lower_note_head: bool = False


@dataclasses.dataclass()
class Fermata(music_parameters.abc.ImplicitPlayingIndicator):
    fermata_type: typing.Optional[
        music_parameters.constants.FERMATA_TYPE_LITERAL
    ] = None


@dataclasses.dataclass()
class Hairpin(music_parameters.abc.ImplicitPlayingIndicator):
    symbol: typing.Optional[music_parameters.constants.HAIRPIN_SYMBOL_LITERAL] = None


@dataclasses.dataclass()
class Trill(music_parameters.abc.ImplicitPlayingIndicator):
    pitch: typing.Optional[music_parameters.abc.Pitch] = None


@dataclasses.dataclass
class PlayingIndicatorCollection(
    music_parameters.abc.IndicatorCollection[music_parameters.abc.PlayingIndicator]
):
    # this is kind of redundant, but perhaps still better than without using
    # the `dataclasses` module
    articulation: Articulation = dataclasses.field(default_factory=Articulation)
    artifical_harmonic: ArtificalHarmonic = dataclasses.field(
        default_factory=ArtificalHarmonic
    )
    arpeggio: Arpeggio = dataclasses.field(default_factory=Arpeggio)
    bartok_pizzicato: music_parameters.abc.PlayingIndicator = dataclasses.field(
        default_factory=music_parameters.abc.ExplicitPlayingIndicator
    )
    bend_after: BendAfter = dataclasses.field(default_factory=BendAfter)
    breath_mark: music_parameters.abc.PlayingIndicator = dataclasses.field(
        default_factory=music_parameters.abc.ExplicitPlayingIndicator
    )
    duration_line_dashed: music_parameters.abc.PlayingIndicator = dataclasses.field(
        default_factory=music_parameters.abc.ExplicitPlayingIndicator
    )
    duration_line_triller: music_parameters.abc.PlayingIndicator = dataclasses.field(
        default_factory=music_parameters.abc.ExplicitPlayingIndicator
    )
    fermata: Fermata = dataclasses.field(default_factory=Fermata)
    glissando: music_parameters.abc.PlayingIndicator = dataclasses.field(
        default_factory=music_parameters.abc.ExplicitPlayingIndicator
    )
    hairpin: Hairpin = dataclasses.field(default_factory=Hairpin)
    natural_harmonic: music_parameters.abc.PlayingIndicator = dataclasses.field(
        default_factory=music_parameters.abc.ExplicitPlayingIndicator
    )
    laissez_vibrer: music_parameters.abc.PlayingIndicator = dataclasses.field(
        default_factory=music_parameters.abc.ExplicitPlayingIndicator
    )
    ornamentation: Ornamentation = dataclasses.field(default_factory=Ornamentation)
    pedal: Pedal = dataclasses.field(default_factory=Pedal)
    prall: music_parameters.abc.PlayingIndicator = dataclasses.field(
        default_factory=music_parameters.abc.ExplicitPlayingIndicator
    )
    precise_natural_harmonic: PreciseNaturalHarmonic = dataclasses.field(
        default_factory=PreciseNaturalHarmonic
    )
    string_contact_point: StringContactPoint = dataclasses.field(
        default_factory=StringContactPoint
    )
    tie: music_parameters.abc.PlayingIndicator = dataclasses.field(
        default_factory=music_parameters.abc.ExplicitPlayingIndicator
    )
    tremolo: Tremolo = dataclasses.field(default_factory=Tremolo)
    trill: Trill = dataclasses.field(default_factory=Trill)

    def __setattr__(self, parameter_name: str, value: bool):
        """Overriding default behaviour to allow syntactic sugar.

        This method allows syntax like:

            playing_indicator_collection.tie = True

        which is the same as

            playing_indicator_collection.tie.is_active = True

        Furthermore the methods makes sure that no property
        can actually be overridden.
        """

        try:
            playing_indicator = getattr(self, parameter_name)
        except AttributeError:
            playing_indicator = None
        if playing_indicator is not None:
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
