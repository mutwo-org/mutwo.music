"""Define ambitus between two pitches"""

from mutwo import music_parameters

__all__ = ("OctaveAmbitus",)


class OctaveAmbitus(music_parameters.abc.PitchAmbitus):
    def pitch_to_period(
        self, pitch: music_parameters.abc.Pitch
    ) -> music_parameters.abc.PitchInterval:
        if isinstance(pitch, music_parameters.JustIntonationPitch):
            return music_parameters.JustIntonationPitch("2/1")
        else:
            return music_parameters.DirectPitchInterval(1200)
