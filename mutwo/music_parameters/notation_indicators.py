"""Define notation indicators for chronons.

This submodules provides several classes to express notation
specifications for :class:`mutwo.core_events.Chronon` objects.
They mostly derive from traditional Western notation.
Unlike playing indicators (see 'mutwo/music_parameters/playing_indicators.py')
module, notation indicators shouldn't have an effect on the played music
and are merely specifications of representation. The proper way to handle
notation indicators should be via a :class:`NotationIndicatorCollection`
object that should be attached to the respective :class:`Chronon`.
The collection contains all possible notation indicators which are defined
in this module. :class:`mutwo.music_events.NoteLike` contain by default
a notation indicator collection.

Notation indicators have one or more arguments. Their :attr:`is_active`
attribute can't be set by the user and get automatically initialised depending
on if all necessary attributes are defined (then active) or if any of the
necessary attributes is set to :obj:`None` (then not active).

**Example:**

Set notation indicators of :class:`NoteLike`:

>>> from mutwo import music_events
>>> my_note = music_events.NoteLike('c', 1 / 4, 'mf')
>>> my_note.notation_indicator_collection.margin_markup.content = "Violin"
"""

import dataclasses
import inspect
import typing

from mutwo import music_parameters


class NotationIndicatorCollection(
    music_parameters.abc.IndicatorCollection[music_parameters.abc.NotationIndicator]
):
    """Collection of notation indicators"""


r = NotationIndicatorCollection.register
implicit = lambda cls: r(dataclasses.dataclass()(cls))


@implicit
class BarLine(music_parameters.abc.NotationIndicator):
    abbreviation: typing.Optional[
        str
    ] = None  # TODO(for future usage add typing.Literal)


@implicit
class Clef(music_parameters.abc.NotationIndicator):
    name: typing.Optional[str] = None  # TODO(for future usage add typing.Literal)


@implicit
class Ottava(music_parameters.abc.NotationIndicator):
    octave_count: typing.Optional[int] = 0


@implicit
class MarginMarkup(music_parameters.abc.NotationIndicator):
    content: typing.Optional[str] = None
    context: typing.Optional[str] = "Staff"  # TODO(for future usage add typing.Literal)


@implicit
class Markup(music_parameters.abc.NotationIndicator):
    content: typing.Optional[str] = None
    direction: typing.Optional[str] = None


@implicit
class RehearsalMark(music_parameters.abc.NotationIndicator):
    markup: typing.Optional[str] = None


# Dynamically define __all__ in order to catch all NotationIndicator classes
__all__ = tuple(
    name
    for name, cls in globals().items()
    if inspect.isclass(cls)
    and music_parameters.abc.NotationIndicator in inspect.getmro(cls)
) + ("NotationIndicatorCollection",)
