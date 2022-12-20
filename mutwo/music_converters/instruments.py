from mutwo import core_converters
from mutwo import core_parameters


__all__ = ("InstrumentNoteLikeToPitchedNoteLike",)


class InstrumentNoteLikeToPitchedNoteLike(
    core_converters.abc.SymmetricalEventConverter
):
    def __init__(self, instrument_to_pitch_dict):
        self.instrument_to_pitch_dict = instrument_to_pitch_dict

    def _convert_simple_event(self, event_to_convert, absolute_time):
        instrument = getattr(event_to_convert, "instrument", None)
        if instrument is not None:
            pitch_list = [self.instrument_to_pitch_dict[instrument]]
            return event_to_convert.copy().set_parameter("pitch_list", pitch_list)
        return event_to_convert

    def convert(self, event_to_convert):
        return self._convert_event(event_to_convert, core_parameters.DirectDuration(0))
