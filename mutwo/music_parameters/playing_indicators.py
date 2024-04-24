"""Define playing indicators for chronons.

This submodules provides several classes to add specific musical
playing techniques to :class:`mutwo.core_events.Chronon` objects.
They mostly derive from traditional Western playing techniques and their
notation. Unlike indicators of the :mod:`mutwo.music_parameters.notation_indicators`
module, playing indicators have an effect on the played music and aren't
merely specifications of representation. The proper way to handle
playing  indicators should be via a :class:`PlayingIndicatorCollection`
object that should be attached to the respective :class:`Chronon`.
The collection contains all possible playing indicators which are defined
in this module. :class:`mutwo.music_events.NoteLike` contain by default
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

Attach :class:`PlayingIndicatorCollection` to :class:`Chronon`:

>>> from mutwo import core_events
>>> from mutwo import music_parameters
>>> my_chronon = core_events.Chronon(1)
>>> my_chronon.playing_indicator_collection = music_parameters.PlayingIndicatorCollection()
"""

import dataclasses
import inspect
import typing

from mutwo import music_parameters


class PlayingIndicatorCollection(
    music_parameters.abc.IndicatorCollection[music_parameters.abc.PlayingIndicator]
):
    """Collection of playing indicators"""

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
                return
        super().__setattr__(parameter_name, value)


r = PlayingIndicatorCollection.register

# Add explicit playing indicators
for exp in (
    "bartok_pizzicato",
    "breath_mark",
    "duration_line_dashed",
    "duration_line_triller",
    "flageolet",
    "glissando",
    "laissez_vibrer",
    "optional",
    "prall",
    "tie",
):
    r(music_parameters.abc.ExplicitPlayingIndicator, exp)
del exp


implicit = lambda cls: r(dataclasses.dataclass()(cls))


# Add implicit playing indicators
@implicit
class Tremolo(music_parameters.abc.ImplicitPlayingIndicator):
    flag_count: typing.Optional[int] = None


@implicit
class Articulation(music_parameters.abc.ImplicitPlayingIndicator):
    name: typing.Optional[music_parameters.constants.ARTICULATION_LITERAL] = None


@implicit
class Arpeggio(music_parameters.abc.ImplicitPlayingIndicator):
    direction: typing.Optional[music_parameters.constants.DIRECTION_LITERAL] = None


@implicit
class Pedal(music_parameters.abc.ImplicitPlayingIndicator):
    type: typing.Optional[music_parameters.constants.PEDAL_TYPE_LITERAL] = None
    activity: typing.Optional[bool] = True


@implicit
class Slur(music_parameters.abc.ImplicitPlayingIndicator):
    activity: typing.Optional[bool] = None


@implicit
class StringContactPoint(music_parameters.abc.ImplicitPlayingIndicator):
    contact_point: typing.Optional[
        music_parameters.constants.CONTACT_POINT_LITERAL
    ] = None


@implicit
class Ornamentation(music_parameters.abc.ImplicitPlayingIndicator):
    direction: typing.Optional[music_parameters.constants.DIRECTION_LITERAL] = None
    count: int = 1


@implicit
class BendAfter(music_parameters.abc.ImplicitPlayingIndicator):
    # Content music_parameters
    bend_amount: typing.Optional[float] = None
    # Presentation music_parameters
    minimum_length: typing.Optional[float] = 3
    thickness: typing.Optional[float] = 3


@implicit
class ArtificalHarmonic(music_parameters.abc.ImplicitPlayingIndicator):
    semitone_count: typing.Optional[int] = None


@implicit
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


@implicit
class Fermata(music_parameters.abc.ImplicitPlayingIndicator):
    type: typing.Optional[music_parameters.constants.FERMATA_TYPE_LITERAL] = None


@implicit
class Hairpin(music_parameters.abc.ImplicitPlayingIndicator):
    symbol: typing.Optional[music_parameters.constants.HAIRPIN_SYMBOL_LITERAL] = None
    niente: bool = False


@implicit
class Trill(music_parameters.abc.ImplicitPlayingIndicator):
    pitch: typing.Optional[music_parameters.abc.Pitch] = None


@implicit
class WoodwindFingering(music_parameters.abc.ImplicitPlayingIndicator):
    cc: typing.Optional[typing.Tuple[str, ...]] = None
    left_hand: typing.Optional[typing.Tuple[str, ...]] = None
    right_hand: typing.Optional[typing.Tuple[str, ...]] = None
    instrument: str = "clarinet"


@implicit
class Cue(music_parameters.abc.ImplicitPlayingIndicator):
    """Cue for electronics etc."""

    index: typing.Optional[int] = None


# Dynamically define __all__ in order to catch all PlayingIndicator classes
__all__ = tuple(
    name
    for name, cls in globals().items()
    if inspect.isclass(cls)
    and music_parameters.abc.PlayingIndicator in inspect.getmro(cls)
) + ("PlayingIndicatorCollection",)
