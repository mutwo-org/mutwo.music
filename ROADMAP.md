## 1.0.0

### Cleanup
- all scale related code


## 0.24.0

### New feature
- allow semantically correct adding/subtracting of `WesternPitchInterval` (see https://github.com/levinericzimmermann/project/blob/10.2/project/patches/music_parameters.py#L125-L181)

### For the sake of completeness
- document all parameters of `NoteLike`
- add more predefined instruments (perhaps all orchestral instruments)
- add type hints to [InstrumentNoteLikeToPitchedNoteLike](https://github.com/mutwo-org/mutwo.music/blob/main/mutwo/music_converters/instruments.py)

### Cosmetics
- simplify code in https://github.com/mutwo-org/mutwo.music/blob/main/mutwo/music_parameters/constants/pitch_intervals.py#L1-L53 by using enums