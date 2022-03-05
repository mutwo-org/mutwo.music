"""Define notation indicators for simple events.

This submodules provides several classes to express notation
specifications for :class:`mutwo.core_events.SimpleEvent` objects.
They mostly derive from traditional Western notation.
Unlike indicators of the :mod:`mutwo.music_parameters.notation_indicators`
module, notation indicators shouldn't have an effect on the played music
and are merely specifications of representation. The proper way to handle
notation indicators should be via a :class:`NotationIndicatorCollection`
object that should be attached to the respective :class:`SimpleEvent`.
The collection contains all possible notation indicators which are defined
in this module. :class:`mutwo.music_events.NoteLike` contain by default
a notation indicator collection.

Notation indicators have one or more arguments. Their :attr:`is_active`
attribute can't be set by the user and get automatically initialised depending
on if all necessary attributes are defined (then active) or if any of the
necessary attributes is set to :obj:`None` (then not active).

**Example:**

Set notation indicators of :class:`NoteLike`:

>>> from mutwo.events import music_events
>>> my_note = music_events.NoteLike('c', 1 / 4, 'mf')
>>> my_note.notation_indicator_collection.margin_markup.content = "Violin"
"""

import dataclasses
import inspect
import typing

from mutwo import music_parameters


@dataclasses.dataclass()
class BarLine(music_parameters.abc.NotationIndicator):
    abbreviation: typing.Optional[
        str
    ] = None  # TODO(for future usage add typing.Literal)


@dataclasses.dataclass()
class Clef(music_parameters.abc.NotationIndicator):
    name: typing.Optional[str] = None  # TODO(for future usage add typing.Literal)


@dataclasses.dataclass()
class Ottava(music_parameters.abc.NotationIndicator):
    n_octaves: typing.Optional[int] = 0


@dataclasses.dataclass()
class MarginMarkup(music_parameters.abc.NotationIndicator):
    content: typing.Optional[str] = None
    context: typing.Optional[str] = "Staff"  # TODO(for future usage add typing.Literal)


@dataclasses.dataclass()
class Markup(music_parameters.abc.NotationIndicator):
    content: typing.Optional[str] = None
    direction: typing.Optional[str] = None


@dataclasses.dataclass()
class RehearsalMark(music_parameters.abc.NotationIndicator):
    markup: typing.Optional[str] = None


@dataclasses.dataclass
class NotationIndicatorCollection(
    music_parameters.abc.IndicatorCollection[music_parameters.abc.NotationIndicator]
):
    bar_line: BarLine = dataclasses.field(default_factory=BarLine)
    clef: Clef = dataclasses.field(default_factory=Clef)
    ottava: Ottava = dataclasses.field(default_factory=Ottava)
    margin_markup: MarginMarkup = dataclasses.field(default_factory=MarginMarkup)
    markup: Markup = dataclasses.field(default_factory=Markup)
    rehearsal_mark: RehearsalMark = dataclasses.field(default_factory=RehearsalMark)

    def __setattr__(self, parameter_name: str, value: bool):
        try:
            notation_indicator = getattr(self, parameter_name)
        except AttributeError:
            notation_indicator = None
        if notation_indicator is not None:
            message = f"Can't override frozen property (notation indicator) '{notation_indicator}'!"
            raise dataclasses.FrozenInstanceError(message)
        else:
            super().__setattr__(parameter_name, value)


# Dynamically define __all__ in order to catch all PlayingIndicator classes
__all__ = tuple(
    name
    for name, cls in globals().items()
    if inspect.isclass(cls)
    and music_parameters.abc.NotationIndicator in inspect.getmro(cls)
) + ("NotationIndicatorCollection",)
