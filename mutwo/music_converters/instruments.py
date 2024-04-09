from mutwo import core_converters
from mutwo import core_events
from mutwo import core_parameters
from mutwo import music_parameters


__all__ = ("InstrumentNoteLikeToPitchedNoteLike",)


class InstrumentNoteLikeToPitchedNoteLike(
    core_converters.abc.SymmetricalEventConverter
):
    def __init__(
        self,
        instrument_to_pitch_dict: dict[
            music_parameters.abc.Instrument, music_parameters.abc.Pitch
        ],
    ):
        self.instrument_to_pitch_dict = instrument_to_pitch_dict

    def _convert_chronon(
        self,
        event_to_convert: core_events.Chronon,
        absolute_time: core_parameters.abc.Duration.Type,
    ):
        instrument = getattr(event_to_convert, "instrument", None)
        if instrument is not None:
            pitch_list = [self.instrument_to_pitch_dict[instrument]]
            return event_to_convert.copy().set_parameter("pitch_list", pitch_list)
        return event_to_convert

    def convert(self, event_to_convert: core_events.abc.Event):
        return self._convert_event(event_to_convert, core_parameters.DirectDuration(0))
