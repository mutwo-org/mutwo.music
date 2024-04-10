"""Set default values for :class:`mutwo.music_events.NoteLike`."""

from mutwo import music_parameters

DEFAULT_PLAYING_INDICATORS_COLLECTION_CLASS = (
    music_parameters.PlayingIndicatorCollection
)
"""Default value for :attr:`mutwo.music_events.NoteLike.playing_indicator_collection`
in :class:`~mutwo.music_events.NoteLike`"""

DEFAULT_NOTATION_INDICATORS_COLLECTION_CLASS = (
    music_parameters.NotationIndicatorCollection
)
"""Default value for :attr:`mutwo.music_events.NoteLike.notation_indicator_collection`
in :class:`~mutwo.music_events.NoteLike`"""
