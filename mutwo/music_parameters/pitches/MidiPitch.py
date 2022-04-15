from __future__ import annotations

from mutwo import core_utilities
from mutwo import music_parameters

__all__ = ("MidiPitch",)


class MidiPitch(music_parameters.abc.Pitch):
    """Pitch that is defined by its midi pitch number.

    :param midi_pitch_number: The midi pitch number of the pitch. Floating
        point numbers are possible for microtonal deviations from the
        chromatic scale.
    :type midi_pitch_number: float

    **Example:**

    >>> from mutwo.music_parameters import pitches
    >>> middle_c = pitches.MidiPitch(60)
    >>> middle_c_quarter_tone_high = pitches.MidiPitch(60.5)
    """

    def __init__(self, midi_pitch_number: float, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._midi_pitch_number = midi_pitch_number

    def __repr__(self) -> str:
        return f"{type(self).__name__}(midi_pitch_number = {self.midi_pitch_number})"

    @property
    def frequency(self) -> float:
        difference_to_middle_a = self.midi_pitch_number - 69
        return float(440 * self.cents_to_ratio(difference_to_middle_a * 100))

    @property
    def midi_pitch_number(self) -> float:
        return self._midi_pitch_number

    @midi_pitch_number.setter
    def midi_pitch_number(self, new_midi_pitch_number: float):
        self._midi_pitch_number = new_midi_pitch_number

    @core_utilities.add_copy_option
    def add(
        self, pitch_interval: music_parameters.abc.PitchInterval, mutate: bool = False
    ) -> MidiPitch:
        self.midi_pitch_number = self.hertz_to_midi_pitch_number(
            self.cents_to_ratio(pitch_interval.interval) * self.frequency
        )
        return self
